#!/usr/bin/env node
/**
 * 用法：node generate-sitemap.js --dir ./dist --domain https://example.com
 *       node generate-sitemap.js --help
 *
 * 扫描指定目录下所有 .html 文件，生成 sitemap.xml 到当前目录。
 * 零 npm 依赖，只用 Node.js 内置模块。
 */

const fs = require('fs');
const path = require('path');

function printHelp() {
  console.log(`
Usage: node generate-sitemap.js --dir <dir> --domain <domain> [--output <file>]

Options:
  --dir      Directory to scan for .html files (required)
  --domain   Base URL of your site, e.g. https://example.com (required)
  --output   Output file path (default: sitemap.xml)
  --help     Show this help
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--help') { args.help = true; continue; }
    if (argv[i].startsWith('--')) {
      args[argv[i].slice(2)] = argv[i + 1];
      i++;
    }
  }
  return args;
}

function walkHtml(dir, baseDir) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkHtml(fullPath, baseDir));
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      files.push(fullPath);
    }
  }
  return files;
}

function htmlPathToUrl(filePath, baseDir, domain) {
  let rel = path.relative(baseDir, filePath).replace(/\\/g, '/');
  // index.html → /  |  foo/index.html → /foo/  |  foo/bar.html → /foo/bar
  if (rel === 'index.html') return domain + '/';
  if (rel.endsWith('/index.html')) return domain + '/' + rel.slice(0, -'index.html'.length);
  if (rel.endsWith('.html')) rel = rel.slice(0, -'.html');
  return domain + '/' + rel;
}

function getLastMod(filePath) {
  const stat = fs.statSync(filePath);
  return stat.mtime.toISOString().slice(0, 10);
}

function buildSitemap(urls) {
  const entries = urls.map(({ url, lastmod }) => `
  <url>
    <loc>${url}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>${url.endsWith('/') ? '1.0' : '0.8'}</priority>
  </url>`).join('');

  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${entries}
</urlset>
`;
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) { printHelp(); process.exit(0); }

  if (!args.dir || !args.domain) {
    console.error('Error: --dir and --domain are required.\nRun with --help for usage.');
    process.exit(1);
  }

  const dir = path.resolve(args.dir);
  const domain = args.domain.replace(/\/$/, '');
  const output = args.output || 'sitemap.xml';

  if (!fs.existsSync(dir)) {
    console.error(`Error: directory not found: ${dir}`);
    process.exit(1);
  }

  const htmlFiles = walkHtml(dir, dir);
  const urls = htmlFiles.map(f => ({
    url: htmlPathToUrl(f, dir, domain),
    lastmod: getLastMod(f),
  }));

  // Sort: root first, then alphabetically
  urls.sort((a, b) => {
    if (a.url === domain + '/') return -1;
    if (b.url === domain + '/') return 1;
    return a.url.localeCompare(b.url);
  });

  const xml = buildSitemap(urls);
  fs.writeFileSync(output, xml, 'utf8');

  console.log(`Generated ${output} with ${urls.length} URL(s)`);
  urls.forEach(u => console.log(' ', u.url));
}

main();
