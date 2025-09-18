// Pomodoro básico con presets y links de música
// Guarda presets en localStorage por usuario (si window.APP_USER_ID existe) y gestiona modal

(function(){
    const userKey = window.APP_USER_ID ? `pomodoro_presets_user_${window.APP_USER_ID}` : 'pomodoro_presets_guest';
    const musicKey = window.APP_USER_ID ? `pomodoro_music_user_${window.APP_USER_ID}` : 'pomodoro_music_guest';

    // Estado
    let timer = null;
    let remaining = 0; // en segundos
    let mode = 'work'; // work | short | long
    let running = false;
    let currentPreset = null;
    let cachedPresets = [];
    let workCycles = 0; // cuántos work se completaron consecutivos

    // Elementos DOM
    const timeEl = document.getElementById('pomodoro-time');
    const startBtn = document.getElementById('start-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const resetBtn = document.getElementById('reset-btn');
    const presetsContainer = document.getElementById('presets-container');
    const openConfig = document.getElementById('open-config');
    const pomodoroModal = document.getElementById('pomodoro-modal');
    const closePomModal = document.getElementById('close-pomodoro-modal');

    const musicLinksEl = document.getElementById('music-links');
    const musicInput = document.getElementById('music-link-input');
    const addMusicBtn = document.getElementById('add-music-link');

    // Config modal elements
    const presetName = document.getElementById('preset-name');
    const presetWork = document.getElementById('preset-work');
    const presetShort = document.getElementById('preset-short');
    const presetLong = document.getElementById('preset-long');
    const colorWork = document.getElementById('color-work');
    const colorShort = document.getElementById('color-short');
    const colorLong = document.getElementById('color-long');
    const configMusicLinks = document.getElementById('config-music-links');
    const configMusicInput = document.getElementById('config-music-input');
    const configAddMusic = document.getElementById('config-add-music');
    const savePresetBtn = document.getElementById('save-preset');
    const deletePresetBtn = document.getElementById('delete-preset');
    const configPresetsList = document.getElementById('config-presets-list');

    // Sonidos simples usando WebAudio
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playBeep(freq = 880, duration = 0.15) {
        try {
            const o = audioCtx.createOscillator();
            const g = audioCtx.createGain();
            o.type = 'sine';
            o.frequency.value = freq;
            o.connect(g);
            g.connect(audioCtx.destination);
            o.start();
            g.gain.setValueAtTime(0.001, audioCtx.currentTime);
            g.gain.exponentialRampToValueAtTime(0.2, audioCtx.currentTime + 0.01);
            setTimeout(() => { o.stop(); }, duration * 1000);
        } catch (e) {
            console.warn('No se pudo reproducir beep', e);
        }
    }

    async function loadPresets(){
        try {
            const res = await fetch('/api/pomodoro/presets');
            if(res.ok){
                const data = await res.json();
                cachedPresets = data;
                return data;
            }
        } catch(e){ console.warn('Error cargando presets', e); }
        cachedPresets = [];
        return [];
    }
    async function createPresetOnServer(obj){
        try {
            const res = await fetch('/api/pomodoro/presets', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(obj)
            });
            if(res.ok) return await res.json();
            const err = await res.json();
            throw new Error(err.error || 'Error creating preset');
        } catch(e){ throw e; }
    }
    async function deletePresetOnServer(id){
        try {
            const res = await fetch(`/api/pomodoro/presets/${id}`, { method: 'DELETE' });
            return res.ok;
        } catch(e){ return false; }
    }

    function loadMusic(){
        const raw = localStorage.getItem(musicKey);
        if(!raw) return [];
        try { return JSON.parse(raw); } catch(e){ return []; }
    }
    function saveMusic(list){
        localStorage.setItem(musicKey, JSON.stringify(list));
    }

    // UI helpers
    function formatTime(sec){
        const m = Math.floor(sec/60).toString().padStart(2,'0');
        const s = (sec%60).toString().padStart(2,'0');
        return `${m}:${s}`;
    }

    async function renderPresets(){
        const presets = await loadPresets();
        presetsContainer.innerHTML = '';
        presets.forEach((p, idx) => {
            const btn = document.createElement('button');
            btn.textContent = p.name || `Preset ${idx+1}`;
            btn.style.marginRight = '8px';
            btn.addEventListener('click', () => {
                applyPreset(p);
                currentPreset = p.id || idx;
            });
            presetsContainer.appendChild(btn);
        });

        // también render en modal
        configPresetsList.innerHTML = '';
        presets.forEach((p, idx)=>{
            const div = document.createElement('div');
            div.style.display = 'flex';
            div.style.justifyContent = 'space-between';
            div.style.alignItems = 'center';
            div.style.padding = '6px 0';
            div.innerHTML = `<div>${p.name}</div>`;
            const loadBtn = document.createElement('button');
            loadBtn.textContent = 'Cargar';
            loadBtn.addEventListener('click', ()=>{ applyPreset(p); pomodoroModal.style.display='none'; });
            const editBtn = document.createElement('button');
            editBtn.textContent = 'Editar';
            editBtn.style.marginLeft = '6px';
            editBtn.addEventListener('click', ()=>{ loadPresetToForm(p, p.id); });
            const delBtn = document.createElement('button');
            delBtn.textContent = 'Eliminar';
            delBtn.style.marginLeft = '6px';
            delBtn.addEventListener('click', async ()=>{
                if(!confirm('Eliminar preset?')) return;
                const ok = await deletePresetOnServer(p.id);
                if(ok) { renderPresets(); } else { alert('Error eliminando preset'); }
            });
            div.appendChild(loadBtn);
            div.appendChild(editBtn);
            div.appendChild(delBtn);
            configPresetsList.appendChild(div);
        });
    }

    function renderMusicLinks(){
        const list = loadMusic();
        musicLinksEl.innerHTML = '';
        configMusicLinks.innerHTML = '';
        list.forEach((u,i)=>{
            const tag = document.createElement('div');
            tag.className = 'tag';
            tag.style.display = 'inline-flex';
            tag.style.gap = '6px';
            tag.innerHTML = `<a class=\"tag-link\" href=\"${u}\" target=\"_blank\">${u}</a><button class=\"remove-tag\">×</button>`;
            tag.querySelector('.remove-tag').addEventListener('click', ()=>{ removeMusic(i); });
            musicLinksEl.appendChild(tag);

            const tag2 = tag.cloneNode(true);
            tag2.querySelector('.remove-tag').addEventListener('click', ()=>{ removeMusic(i); });
            configMusicLinks.appendChild(tag2);
        });
    }

    function addMusic(url){
        if(!url) return;
        const list = loadMusic();
        list.push(url);
        saveMusic(list);
        renderMusicLinks();
    }
    function removeMusic(i){
        const list = loadMusic();
        list.splice(i,1);
        saveMusic(list);
        renderMusicLinks();
    }

    function applyPreset(p){
        // p: {name, work, short, long, colors: {work, short, long}}
        mode = 'work';
        remaining = (p.work || 25) * 60;
        updateDisplay();
        // aplicar colores
        const card = document.querySelector('.pomodoro-card');
        if(card){
            card.style.background = p.colors && p.colors.work ? p.colors.work : '#fff';
        }
    }

    function loadPresetToForm(p, idx){
        presetName.value = p.name || '';
        presetWork.value = p.work || 25;
        presetShort.value = p.short || 5;
        presetLong.value = p.long || 15;
        colorWork.value = (p.colors && p.colors.work) || '#f56565';
        colorShort.value = (p.colors && p.colors.short) || '#f6ad55';
        colorLong.value = (p.colors && p.colors.long) || '#48bb78';
        currentPreset = idx;
    }

    async function savePreset(){
        // crear preset en servidor, respetar límite de 3
        const obj = {
            name: presetName.value || 'Preset',
            work: parseInt(presetWork.value,10) || 25,
            short: parseInt(presetShort.value,10) || 5,
            long: parseInt(presetLong.value,10) || 15,
            colors: { work: colorWork.value, short: colorShort.value, long: colorLong.value }
        };
        try {
            const created = await createPresetOnServer(obj);
            // refrescar lista
            await renderPresets();
            currentPreset = created.id;
            alert('Preset guardado');
        } catch(e){
            alert(e.message || 'Error al guardar preset');
        }
    }

    async function deletePreset(){
        if(!currentPreset) return;
        const ok = await deletePresetOnServer(currentPreset);
        if(ok){
            currentPreset = null;
            await renderPresets();
        } else alert('No se pudo eliminar preset');
    }

    function updateDisplay(){
        timeEl.textContent = formatTime(remaining);
        // background segun modo
        const card = document.querySelector('.pomodoro-card');
        if(card){
            if(mode === 'work') card.style.background = colorWork.value || '#fff';
            else if(mode === 'short') card.style.background = colorShort.value || '#fff';
            else card.style.background = colorLong.value || '#fff';
        }
            // Removed localStorage publication for pomodoro_status
    }

    function tick(){
        if(remaining <= 0){
            stopTimer();
            // Reproducir alarma configurada o beep por defecto
            try { playAlarm(); } catch(e){ playBeep(1200, 0.4); }
            // pasar al siguiente modo con conteo de ciclos y long break
            if(mode === 'work') {
                workCycles += 1;
                // leer setting de ciclos antes de long
                const cyclesSetting = getCyclesBeforeLong();
                if(workCycles >= cyclesSetting){
                    mode = 'long';
                    remaining = (getCurrentPreset().long||15)*60;
                    workCycles = 0; // reset cycles
                } else {
                    mode = 'short';
                    remaining = (getCurrentPreset().short||5)*60;
                }
            } else if(mode === 'short') {
                mode = 'work';
                remaining = (getCurrentPreset().work||25)*60;
            } else {
                mode = 'work';
                remaining = (getCurrentPreset().work||25)*60;
            }
            updateDisplay();
            return;
        }
        remaining -= 1;
        updateDisplay();
    }

    // Alarm helpers: save/load alarm URL per-user in localStorage
    const alarmKey = window.APP_USER_ID ? `pomodoro_alarm_user_${window.APP_USER_ID}` : 'pomodoro_alarm_guest';
    function getAlarmUrl(){
        try { return localStorage.getItem(alarmKey) || ''; } catch(e){ return ''; }
    }
    function saveAlarmUrl(url){
        try { localStorage.setItem(alarmKey, url || ''); } catch(e){}
    }
    function playAlarm(){
        const url = getAlarmUrl();
        if(url){
            const a = new Audio(url);
            a.play().catch((err)=>{
                console.warn('No se pudo reproducir audio remoto, fallback beep', err);
                playBeep(1200, 0.4);
            });
            return;
        }
        // fallback simple
        playBeep(1200, 0.4);
    }

    function advancePhase(){
        // Forzar paso inmediato a la siguiente fase
        if(mode === 'work'){
            workCycles += 1;
            const cyclesSetting = getCyclesBeforeLong();
            if(workCycles >= cyclesSetting){
                mode = 'long';
                remaining = (getCurrentPreset().long||15)*60;
                workCycles = 0;
            } else {
                mode = 'short';
                remaining = (getCurrentPreset().short||5)*60;
            }
        } else if(mode === 'short'){
            mode = 'work';
            remaining = (getCurrentPreset().work||25)*60;
        } else {
            mode = 'work';
            remaining = (getCurrentPreset().work||25)*60;
        }
        updateDisplay();
        // Si estaba corriendo, reiniciar el contador para la nueva fase
        if(running){
            stopTimer();
            startTimer();
        }
    }

    // Ciclos before long helper (persistido por usuario)
    const cyclesKey = window.APP_USER_ID ? `pomodoro_cycles_user_${window.APP_USER_ID}` : 'pomodoro_cycles_guest';
    function getCyclesBeforeLong(){
        try { const v = parseInt(localStorage.getItem(cyclesKey),10); return isNaN(v) ? 4 : v; } catch(e){ return 4; }
    }
    function saveCyclesBeforeLong(n){ try { localStorage.setItem(cyclesKey, String(n)); } catch(e){} }

    function startTimer(){
        if(running) return;
        running = true;
        if(!remaining) remaining = (getCurrentPreset().work||25)*60;
        timer = setInterval(tick, 1000);
    }
    function stopTimer(){
        running = false;
        if(timer) clearInterval(timer);
        timer = null;
    }
    function pauseTimer(){
        stopTimer();
    }
    function resetTimer(){
        stopTimer();
        remaining = (getCurrentPreset().work||25)*60;
        mode = 'work';
        updateDisplay();
    }

    function getCurrentPreset(){
        const presets = cachedPresets || [];
        if(currentPreset !== null){
            // currentPreset may be an index or an id
            if(typeof currentPreset === 'number'){
                if(presets[currentPreset]) return presets[currentPreset];
            } else {
                const found = presets.find(p=>String(p.id) === String(currentPreset));
                if(found) return found;
            }
        }
        return presets[0] || {name: 'Default', work:25, short:5, long:15, colors:{work: '#f56565', short:'#f6ad55', long:'#48bb78'}};
    }

    // Eventos
    startBtn.addEventListener('click', ()=>{ startTimer(); });
    pauseBtn.addEventListener('click', ()=>{ pauseTimer(); });
    resetBtn.addEventListener('click', ()=>{ resetTimer(); });
    const nextPhaseBtn = document.getElementById('next-phase-btn');
    if(nextPhaseBtn) nextPhaseBtn.addEventListener('click', ()=>{ advancePhase(); });

    addMusicBtn.addEventListener('click', ()=>{ const v = musicInput.value.trim(); if(v){ addMusic(v); musicInput.value=''; } });
    musicInput.addEventListener('keypress', (e)=>{ if(e.key==='Enter'){ e.preventDefault(); addMusic(musicInput.value.trim()); musicInput.value=''; } });
    openConfig.addEventListener('click', ()=>{ pomodoroModal.style.display='flex'; renderPresets(); renderMusicLinks(); });
    document.getElementById('open-pomodoro-config').addEventListener('click', ()=>{ pomodoroModal.style.display='flex'; renderPresets(); renderMusicLinks(); });
    closePomModal.addEventListener('click', ()=>{ pomodoroModal.style.display='none'; });
    pomodoroModal.addEventListener('click', (e)=>{ if(e.target===pomodoroModal) pomodoroModal.style.display='none'; });

    // Cargar alarm URL cuando se abre la configuración
    const alarmUrlInput = document.getElementById('alarm-url');
    const testAlarmBtn = document.getElementById('test-alarm');
    const saveAlarmBtn = document.getElementById('save-alarm');
    function loadAlarmIntoForm(){ if(alarmUrlInput) alarmUrlInput.value = getAlarmUrl() || ''; }
    if(openConfig){ openConfig.addEventListener('click', loadAlarmIntoForm); }
    if(document.getElementById('open-pomodoro-config')) document.getElementById('open-pomodoro-config').addEventListener('click', loadAlarmIntoForm);
    if(testAlarmBtn) testAlarmBtn.addEventListener('click', ()=>{ playAlarm(); });
    if(saveAlarmBtn) saveAlarmBtn.addEventListener('click', ()=>{ if(alarmUrlInput) saveAlarmUrl(alarmUrlInput.value.trim()); alert('Alarma guardada'); });

    // cycles-before-long input binding
    const cyclesInput = document.getElementById('cycles-before-long');
    function loadCyclesIntoForm(){ if(cyclesInput) cyclesInput.value = getCyclesBeforeLong(); }
    if(openConfig){ openConfig.addEventListener('click', loadCyclesIntoForm); }
    if(document.getElementById('open-pomodoro-config')) document.getElementById('open-pomodoro-config').addEventListener('click', loadCyclesIntoForm);
    if(cyclesInput) cyclesInput.addEventListener('change', ()=>{ const v = parseInt(cyclesInput.value,10); if(!isNaN(v) && v>0) saveCyclesBeforeLong(v); });

    configAddMusic.addEventListener('click', ()=>{ const v = configMusicInput.value.trim(); if(v){ addMusic(v); configMusicInput.value=''; } });
    configMusicInput.addEventListener('keypress', (e)=>{ if(e.key==='Enter'){ e.preventDefault(); const v = configMusicInput.value.trim(); if(v){ addMusic(v); configMusicInput.value=''; } } });

    savePresetBtn.addEventListener('click', ()=>{ savePreset(); });
    deletePresetBtn.addEventListener('click', ()=>{ deletePreset(); });
    // Botón para agregar preset (abre modal limpio)
    const addPresetBtn = document.getElementById('add-preset-btn');
    if(addPresetBtn){
        addPresetBtn.addEventListener('click', ()=>{
            // limpiar formulario
            presetName.value = '';
            presetWork.value = 25;
            presetShort.value = 5;
            presetLong.value = 15;
            colorWork.value = '#f56565';
            colorShort.value = '#f6ad55';
            colorLong.value = '#48bb78';
            currentPreset = null;
            pomodoroModal.style.display = 'flex';
            renderPresets();
        });
    }

    // Inicialización
    (async function init(){
        // si no hay presets, crear default
        const presets = await loadPresets();
        if(presets.length===0){
            // intentar crear preset default en servidor (si hay usuario)
            try {
                await createPresetOnServer({name:'Default', work:25, short:5, long:15, colors:{work:'#f56565', short:'#f6ad55', long:'#48bb78'}});
            } catch(e){ /* permitir fallback */ }
        }
        await renderPresets();
        renderMusicLinks();
        // aplicar preset 0
        // aplicar primer preset si existe
        const all = cachedPresets;
        if(all && all.length>0){ applyPreset(all[0]); currentPreset = all[0].id; }
        updateDisplay();
    })();

})();
