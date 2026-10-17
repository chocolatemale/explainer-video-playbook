/* Paste into a Pexels search-page browser console after reviewing the page's license.
 * No cookies, authorization headers, account IDs or browser state are exported. */
(() => {
  const element = document.querySelector('script#__NEXT_DATA__');
  if (!element) throw new Error('No __NEXT_DATA__; page schema changed. Inspect the page manually.');
  const found = new Map();
  function walk(node) {
    if (!node || typeof node !== 'object') return;
    const id = String(node.id || '');
    const files = node.video_files || node.videoFiles || [];
    const file = files.find(f => /videos\.pexels\.com/.test(f.link || f.src || ''));
    let url = node.video?.src || node.video?.url || file?.link || file?.src || node.src;
    if (/^\d+$/.test(id) && typeof url === 'string' && /^https:\/\/videos\.pexels\.com\//.test(url)) {
      found.set(id, {id, duration: node.duration ?? node.video?.duration ?? null,
        page: `https://www.pexels.com/video/${id}/`, url, beats: []});
    }
    Object.values(node).forEach(walk);
  }
  walk(JSON.parse(element.textContent));
  const rows = [...found.values()];
  if (!rows.length) throw new Error('No matching video records; inspect __NEXT_DATA__ fields.');
  const blob = new Blob([JSON.stringify(rows, null, 2) + '\n'], {type: 'application/json'});
  const url = URL.createObjectURL(blob), link = document.createElement('a');
  link.href = url; link.download = 'pexels-candidates.json'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  console.table(rows);
  return rows;
})();
