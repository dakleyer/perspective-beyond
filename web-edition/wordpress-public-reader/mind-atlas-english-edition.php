<?php
/**
 * Plugin Name: Mind Atlas English Edition
 * Description: Public HTML, text and data routes for the complete Perspective Beyond Atlas.
 * Version: 2026.11.04.4
 * Author: Perspective Beyond
 */
if (!defined('ABSPATH')) { exit; }

add_action('template_redirect', static function () {
    $base = '/atlas-reader';
    $uri = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
    if (!is_string($uri) || ($uri !== $base && strpos($uri, $base . '/') !== 0)) { return; }
    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
    if ($method !== 'GET' && $method !== 'HEAD') { status_header(405); header('Allow: GET, HEAD'); exit; }
    $relative = ltrim(rawurldecode(substr($uri, strlen($base))), '/');
    if (strpos($relative, '..') !== false || strpos($relative, "\0") !== false || strpos($relative, '\\') !== false) { status_header(404); exit; }
    if ($relative === '' || substr($relative, -1) === '/') { $relative .= 'index.html'; }
    $types = ['html' => 'text/html', 'txt' => 'text/plain', 'json' => 'application/json', 'css' => 'text/css', 'xml' => 'application/xml'];
    $extension = strtolower(pathinfo($relative, PATHINFO_EXTENSION));
    // English publication manifest: immutable source and verified local asset.
    $manifestDigest = 'f13a91d5c802bb573c3f3497066cfca81c2fd806b417249e7252247c626f0fa1';
    $manifestCache = wp_upload_dir()['basedir'] . '/mind-atlas-reader/english-' . $manifestDigest . '.json';
    $manifestBody = is_file($manifestCache) ? file_get_contents($manifestCache) : false;
    if ($manifestBody === false || hash('sha256', $manifestBody) !== $manifestDigest) {
        $manifestResponse = wp_remote_get('https://raw.githubusercontent.com/dakleyer/perspective-beyond/158d50b7ced4fd628482565d707c274a0c2a483c/web-edition/wordpress-public-reader/manifest-en.json', ['timeout' => 30, 'redirection' => 0, 'limit_response_size' => 2000000]);
        $manifestBody = is_wp_error($manifestResponse) ? false : wp_remote_retrieve_body($manifestResponse);
        if (!is_string($manifestBody) || hash('sha256', $manifestBody) !== $manifestDigest) { status_header(503); header('Retry-After: 30'); exit; }
        if (wp_mkdir_p(dirname($manifestCache))) { file_put_contents($manifestCache, $manifestBody, LOCK_EX); }
    }
    $manifest = json_decode($manifestBody, true);
    if (!preg_match('~^[a-zA-Z0-9_./-]+$~D', $relative) || !isset($manifest['files'][$relative]) || !isset($types[$extension])) {
        status_header(404); header('Content-Type: text/plain; charset=UTF-8');
        echo 'Atlas: ' . home_url($base . '/') . "\n"; exit;
    }
    $uploads = wp_upload_dir();
    $cache = $uploads['basedir'] . '/mind-atlas-reader/' . $manifest['revision'] . '/' . $relative;
    $body = false;
    if (is_file($cache)) {
        $candidate = file_get_contents($cache);
        if (hash('sha256', $candidate) === $manifest['files'][$relative]['sha256']) { $body = $candidate; }
    }
    if ($body === false) {
        $remotePath = $manifest['files'][$relative]['source'];
        $remote = 'https://raw.githubusercontent.com/dakleyer/perspective-beyond/' . $manifest['revision'] . '/' . $remotePath;
        $response = wp_remote_get($remote, ['timeout' => 30, 'redirection' => 0, 'limit_response_size' => 12000000]);
        if (is_wp_error($response) || wp_remote_retrieve_response_code($response) !== 200) { status_header(503); header('Retry-After: 30'); exit; }
        $body = wp_remote_retrieve_body($response);
        if (hash('sha256', $body) !== $manifest['files'][$relative]['sha256']) { status_header(503); header('Retry-After: 30'); exit; }
        if (wp_mkdir_p(dirname($cache))) { file_put_contents($cache, $body, LOCK_EX); }
    }
    if ($relative !== 'grafo.json' && basename($relative) !== 'registro.json') {
        $body = str_replace('https://dakleyer.github.io/perspective-beyond/atlas/lectura', home_url($base), $body);
        $body = str_replace('/perspective-beyond/atlas/lectura', $base, $body);
        $body = str_replace('https://dakleyer.github.io/perspective-beyond/atlas/mapa/grafo.json', home_url($base . '/grafo.json'), $body);
    }
    status_header(200);
    header('Content-Type: ' . $types[$extension] . '; charset=UTF-8');
    header('X-Robots-Tag: index, follow');
    header('X-Content-Type-Options: nosniff');
    header('Access-Control-Allow-Origin: *');
    header('Cache-Control: public, max-age=300');
    header('Link: <' . home_url($base . '/entrada.txt') . '>; rel="describedby"; type="text/plain"');
    header('X-Atlas-Revision: ' . $manifest['revision']);
    header('X-Atlas-Graph: ' . $manifest['graphSha256']);
    if ($method === 'GET') { echo $body; }
    exit;
}, -1000);

add_action('wp_head', static function () {
    echo '<link rel="alternate" type="text/plain" title="Mind Atlas: assistant entry" href="' . esc_url(home_url('/atlas-reader/entrada.txt')) . '">' . "\n";
    echo '<link rel="sitemap" type="application/xml" title="Mind Atlas: public URLs" href="' . esc_url(home_url('/atlas-reader/sitemap.xml')) . '">' . "\n";
});

add_filter('robots_txt', static function ($output) {
    return rtrim($output) . "\n\nUser-agent: *\nAllow: /atlas-reader/\nSitemap: " . home_url('/atlas-reader/sitemap.xml') . "\n";
}, 20);
