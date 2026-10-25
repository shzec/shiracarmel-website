const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.primary-nav');
if (menuButton && nav) menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('is-open', open);
});
document.querySelectorAll('.primary-nav a').forEach(link => link.addEventListener('click', () => {
  if (menuButton) menuButton.setAttribute('aria-expanded', 'false');
  if (nav) nav.classList.remove('is-open');
}));
document.querySelectorAll('.poem-flip-card').forEach(card => card.addEventListener('click', () => {
  const flipped = card.classList.toggle('is-flipped');
  card.setAttribute('aria-pressed', String(flipped));
  card.setAttribute('aria-label', flipped
    ? 'Poem card, second perspective. Activate to return to the first perspective.'
    : 'Poem card, first perspective. Activate to change perspectives.');
  const front = card.querySelector('.poem-flip-front');
  const back = card.querySelector('.poem-flip-back');
  front?.setAttribute('aria-hidden', String(flipped));
  back?.setAttribute('aria-hidden', String(!flipped));
}));
const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();
document.querySelectorAll('a[href*="ADD_"]').forEach(link => {
  const token = link.getAttribute('href').split('ADD_')[1];
  const map = {ARTIST_EMAIL:'email',INSTAGRAM_URL:'instagram',YOUTUBE_URL:'youtube',SPOTIFY_URL:'spotify',PRESS_PRELISTEN_URL:'pressPrelisten',PRE_SAVE_URL:'presave',PREVIOUS_MUSIC_URL:'previousMusic',OFFICIAL_VIDEO_URL:'officialVideo',LIVE_VIDEO_URL:'liveVideo'};
  const value = window.SITE_CONTENT?.links?.[map[token]];
  if (value && !value.includes('ADD_')) {
    link.href = token === 'ARTIST_EMAIL' ? `mailto:${value.replace(/^mailto:/,'')}` : value;
    link.removeAttribute('aria-disabled');
  } else {
    link.addEventListener('click', event => event.preventDefault());
    link.setAttribute('aria-disabled', 'true');
  }
});
const dates = window.SITE_CONTENT?.tourDates || [];
const tourList = document.getElementById('live-list');
const emptyMessage = document.getElementById('live-empty');
if (tourList && dates.length) {
  emptyMessage?.remove();
  const heading = document.getElementById('live-heading');
  if (heading) heading.textContent = 'Upcoming dates';
  tourList.innerHTML = dates.map(show => `<article class="tour-date"><time datetime="${show.isoDate || ''}">${show.date}</time><span><strong>${show.title || show.venue}</strong><small>${show.venueUrl ? `<a href="${show.venueUrl}" target="_blank" rel="noreferrer">${show.venue} ↗︎</a>` : show.venue}${show.time ? ` · ${show.time}` : ''}</small></span></article>`).join('');
}
const previewPanel = document.getElementById('press-preview');
const previewToggle = document.getElementById('press-download-toggle');
function openPressAudio(focus = false) {
  if (!previewPanel) return;
  previewPanel.hidden = false;
  previewToggle?.setAttribute('aria-expanded', 'true');
  if (focus) document.getElementById('preview-password')?.focus();
}
previewToggle?.addEventListener('click', () => {
  openPressAudio(true);
  previewPanel.scrollIntoView({behavior: 'smooth', block: 'center'});
});
if (location.hash === '#press-preview') openPressAudio();
window.addEventListener('hashchange', () => {
  if (location.hash === '#press-preview') openPressAudio(true);
});
const previewForm = document.getElementById('preview-form');
if (previewForm) previewForm.addEventListener('submit', async event => {
  event.preventDefault();
  const status = document.getElementById('preview-status');
  const player = document.getElementById('preview-audio');
  const download = document.getElementById('preview-download');
  const submit = previewForm.querySelector('button[type="submit"]');
  const password = document.getElementById('preview-password').value;
  status.textContent = 'Unlocking the press audio (65 MB). This may take a moment…';
  submit.disabled = true;
  try {
    const response = await fetch('assets/press-wav.enc');
    if (!response.ok) throw new Error('The press audio is not available right now. Please try again.');
    const bytes = new Uint8Array(await response.arrayBuffer());
    const salt = bytes.slice(0, 16);
    const iv = bytes.slice(16, 28);
    const ciphertext = bytes.slice(28);
    const material = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveKey']);
    const key = await crypto.subtle.deriveKey({name:'PBKDF2',salt,iterations:310000,hash:'SHA-256'}, material, {name:'AES-GCM',length:256}, false, ['decrypt']);
    const audio = await crypto.subtle.decrypt({name:'AES-GCM',iv}, key, ciphertext);
    if (player.dataset.objectUrl) URL.revokeObjectURL(player.dataset.objectUrl);
    const objectUrl = URL.createObjectURL(new Blob([audio], {type:'audio/wav'}));
    player.src = objectUrl;
    player.dataset.objectUrl = objectUrl;
    player.hidden = false;
    download.href = objectUrl;
    download.hidden = false;
    previewForm.hidden = true;
    document.getElementById('preview-password').value = '';
    status.textContent = 'Audio unlocked. Play the song below or download the WAV file.';
  } catch (error) {
    status.textContent = error.name === 'OperationError' ? 'That password did not unlock the audio. Please check it and try again.' : (error.message || 'Unable to unlock the audio. Please try again.');
  } finally {
    submit.disabled = false;
  }
});
window.addEventListener('pagehide', () => {
  const player = document.getElementById('preview-audio');
  if (player?.dataset.objectUrl) URL.revokeObjectURL(player.dataset.objectUrl);
});
