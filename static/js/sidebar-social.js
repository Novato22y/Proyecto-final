// sidebar-social.js
// Sistema dinámico para mostrar redes sociales en el sidebar y modal
console.log('sidebar-social.js loaded');

const socialNetworks = [
  {
    name: 'WhatsApp',
    url: 'https://web.whatsapp.com',
    svg: `<svg viewBox="0 0 16 16" class="socialSvg whatsappSvg"><path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"></path></svg>`
  },
  {
    name: 'Instagram',
    url: 'https://instagram.com',
    svg: `<svg viewBox="0 0 16 16" class="socialSvg instagramSvg"><path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"></path></svg>`
  },

// Ejemplo: cómo añadir otra red social (YouTube)
// Copia el siguiente objeto y pégalo dentro del arreglo `socialNetworks` si deseas agregarlo.
// Asegúrate de usar una URL real en `url` y un SVG optimizado.
// {
//   name: 'YouTube',
//   url: 'https://www.youtube.com/tu_canal',
//   svg: `<svg viewBox="0 0 24 24" class="socialSvg youtubeSvg"><path d="M23.498 6.186a2.998 2.998 0 00-2.11-2.12C19.315 3.333 12 3.333 12 3.333s-7.315 0-9.388.733A2.998 2.998 0 00.501 6.186 31.82 31.82 0 000 12a31.82 31.82 0 00.501 5.814 2.998 2.998 0 002.111 2.12C4.685 20.667 12 20.667 12 20.667s7.315 0 9.388-.733a2.998 2.998 0 002.11-2.12A31.82 31.82 0 0024 12a31.82 31.82 0 00-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"></path></svg>`
// }
  {
    name: 'Twitter',
    url: 'https://x.com',
    svg: `<svg viewBox="0 0 16 16" class="socialSvg twitterSvg"><path d="M5.026 15c6.038 0 9.341-5.003 9.341-9.334 0-.14 0-.282-.006-.422A6.685 6.685 0 0 0 16 3.542a6.658 6.658 0 0 1-1.889.518 3.301 3.301 0 0 0 1.447-1.817 6.533 6.533 0 0 1-2.087.793A3.286 3.286 0 0 0 7.875 6.03a9.325 9.325 0 0 1-6.767-3.429 3.289 3.289 0 0 0 1.018 4.382A3.323 3.323 0 0 1 .64 6.575v.045a3.288 3.288 0 0 0 2.632 3.218 3.203 3.203 0 0 1-.865.115 3.23 3.23 0 0 1-.614-.057 3.283 3.283 0 0 0 3.067 2.277A6.588 6.588 0 0 1 .78 13.58a6.32 6.32 0 0 1-.78-.045A9.344 9.344 0 0 0 5.026 15z"></path></svg>`
  },
  {
    name: 'LinkedIn',
    url: 'https://linkedin.com',
    svg: `<svg viewBox="0 0 448 512" class="socialSvg linkdinSvg"><path d="M100.28 448H7.4V148.9h92.88zM53.79 108.1C24.09 108.1 0 83.5 0 53.8a53.79 53.79 0 0 1 107.58 0c0 29.7-24.1 54.3-53.79 54.3zM447.9 448h-92.68V302.4c0-34.7-.7-79.2-48.29-79.2-48.29 0-55.69 37.7-55.69 76.7V448h-92.78V148.9h89.08v40.8h1.3c12.4-23.5 42.69-48.3 87.88-48.3 94 0 111.28 61.9 111.28 142.3V448z"></path></svg>`
  },

  {
    name: 'Facebook',
    url: 'https://facebook.com',
    svg: `<svg viewBox="0 0 320 512" class="socialSvg facebookSvg"><path d="M279.14 288l14.22-92.66h-88.91V127.89c0-25.35 12.42-50.06 52.24-50.06H293V6.26S259.5 0 225.36 0c-73.22 0-121.09 44.38-121.09 124.72V195.3H22.89V288h81.38v224h100.2V288z"/></svg>`
  },
  {
    name: 'TikTok',
    url: 'https://tiktok.com',
    svg: `<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>TikTok</title><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>`
  },
  {
    name: 'YouTube',
    url: 'https://youtube.com',
    svg: `<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>YouTube</title><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>`
  }
  ,
  {
    name: 'GitHub',
    url: 'https://github.com/tu_usuario',
    svg: `<svg viewBox="0 0 24 24" class="socialSvg githubSvg" xmlns="http://www.w3.org/2000/svg"><path d="M12 .5C5.73.5.5 5.73.5 12c0 5.08 3.29 9.39 7.86 10.93.57.1.78-.25.78-.55 0-.27-.01-1-.02-1.96-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.27-1.69-1.27-1.69-1.04-.71.08-.7.08-.7 1.15.08 1.75 1.18 1.75 1.18 1.02 1.75 2.68 1.24 3.33.95.1-.74.4-1.24.72-1.53-2.56-.29-5.26-1.28-5.26-5.7 0-1.26.45-2.29 1.18-3.1-.12-.29-.51-1.47.11-3.06 0 0 .96-.31 3.15 1.18a10.9 10.9 0 012.87-.39c.97 0 1.95.13 2.87.39 2.19-1.49 3.15-1.18 3.15-1.18.62 1.59.23 2.77.11 3.06.73.81 1.18 1.84 1.18 3.1 0 4.43-2.71 5.41-5.29 5.69.41.35.77 1.04.77 2.1 0 1.52-.01 2.74-.01 3.11 0 .3.21.66.79.55A11.52 11.52 0 0023.5 12C23.5 5.73 18.27.5 12 .5z"/></svg>`
  },
  {
    name: 'Discord',
    url: 'https://discord.gg/tu_invitacion',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-discord socialSvg discordSvg" viewBox="0 0 16 16">
  <path d="M13.545 2.907a13.2 13.2 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.2 12.2 0 0 0-3.658 0 8 8 0 0 0-.412-.833.05.05 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.04.04 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032q.003.022.021.037a13.3 13.3 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019q.463-.63.818-1.329a.05.05 0 0 0-.01-.059l-.018-.011a9 9 0 0 1-1.248-.595.05.05 0 0 1-.02-.066l.015-.019q.127-.095.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.05.05 0 0 1 .053.007q.121.1.248.195a.05.05 0 0 1-.004.085 8 8 0 0 1-1.249.594.05.05 0 0 0-.03.03.05.05 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.2 13.2 0 0 0 4.001-2.02.05.05 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.03.03 0 0 0-.02-.019m-8.198 7.307c-.789 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612m5.316 0c-.788 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612"/>
</svg>`
  }
];

// estado local que puede venir del servidor
// no remote socials in restored version
let remoteSocials = null;

function renderSocialIcons() {
  const sidebar = document.getElementById('sidebar-social-icons');
  const modal = document.getElementById('modal-social-icons');
  const moreBtn = document.getElementById('open-social-modal');
  if (!sidebar || !modal || !moreBtn) return;
  sidebar.innerHTML = '';
  modal.innerHTML = '';
  const nameMap = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten'];
  socialNetworks.slice(0, 4).forEach((net, i) => {
    const a = document.createElement('a');
    const suffix = nameMap[i] || (i + 1);
    a.className = 'enlace-icono social-dynamic-icon container' + suffix;
    a.href = net.url;
    a.title = net.name;
    a.innerHTML = net.svg;
    // Asegurar que el SVG insertado tenga la clase `socialSvg` y que sus paths usen fill="currentColor"
    const svgElSidebar = a.querySelector('svg');
    if (svgElSidebar) {
      if (!svgElSidebar.classList.contains('socialSvg')) svgElSidebar.classList.add('socialSvg');
      svgElSidebar.querySelectorAll('path').forEach(p => {
        // solo sobrescribe fills fijos para permitir heredar color desde CSS
        const fill = p.getAttribute('fill');
        if (!fill || fill === '' || fill.toLowerCase() === 'none' || fill === 'currentColor') {
          p.setAttribute('fill', 'currentColor');
        } else {
          // reemplaza fills hexadecimales o rgb por currentColor
          p.setAttribute('fill', 'currentColor');
        }
      });
    }
    sidebar.appendChild(a);
  });
  moreBtn.style.display = '';
  socialNetworks.slice(4).forEach((net, i) => {
    const a = document.createElement('a');
    const suffix = nameMap[i + 4] || (i + 5);
    a.className = 'socialContainer container' + suffix;
    a.href = net.url;
    a.title = net.name;
    a.innerHTML = net.svg;
    // Asegurar que el SVG insertado en el modal tenga la clase `socialSvg` y paths con fill=currentColor
    const svgElModal = a.querySelector('svg');
    if (svgElModal) {
      if (!svgElModal.classList.contains('socialSvg')) svgElModal.classList.add('socialSvg');
      svgElModal.querySelectorAll('path').forEach(p => {
        p.setAttribute('fill', 'currentColor');
      });
    }
    modal.appendChild(a);
  });
}
document.addEventListener('DOMContentLoaded', function() {
  renderSocialIcons();
  const moreBtn = document.getElementById('open-social-modal');
  const modalLateral = document.getElementById('social-modal');
  const closeBtn = document.querySelector('.close-lateral-modal');
  if (moreBtn && modalLateral) {
    moreBtn.addEventListener('click', function(e) {
      e.preventDefault();
      modalLateral.classList.add('visible');
    });
  }
  if (closeBtn && modalLateral) {
    closeBtn.addEventListener('click', function() {
      modalLateral.classList.remove('visible');
    });
  }
  window.addEventListener('click', function(e) {
    if (e.target === modalLateral) {
      modalLateral.classList.remove('visible');
    }
  });
});
