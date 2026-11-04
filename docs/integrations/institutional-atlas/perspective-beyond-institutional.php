<?php
/**
 * Plugin Name: Perspective Beyond — Atlas institucional
 * Description: Mapas de lectura contextuales para Integral Management y el Instituto del Totonacapan.
 * Version: 1.3.0
 * License: GPL-2.0-or-later
 */
if (!defined('ABSPATH')) { exit; }
final class PB_Institutional_Visual_Entries_V13 {
 private static $rendered = false;
 private static $data = null;
 private static function site() {
  $host = strtolower((string) wp_parse_url(home_url('/'), PHP_URL_HOST));
  return $host === 'integralmanagement.ch' ? 'imsv' : ($host === 'totonacapan.com' ? 'totonacapan' : '');
 }
 private static function allowed() { return self::site() && !is_admin() && !is_feed() && !(defined('REST_REQUEST') && REST_REQUEST); }
 public static function assets() {
  if (!self::allowed()) { return; }
  wp_enqueue_style('pb-institutional-atlas', plugins_url('atlas.css', __FILE__), array(), '1.3.0');
  wp_enqueue_script('pb-institutional-atlas', plugins_url('atlas.js', __FILE__), array(), '1.3.0', true);
 }
 private static function data() {
  if (self::$data === null) { self::$data = json_decode((string) file_get_contents(__DIR__ . '/registry.json'), true); }
  return self::$data;
 }
 private static function labels($lang) {
  $all = array(
   'es'=>array('Ideas que conversan con esta página','Una entrada al Atlas de pensamiento','El Atlas relaciona páginas, ideas, experiencias y fuentes. Este mapa parte de la lectura actual y abre un recorrido por sus vecinos conceptuales.','Abrir el mapa y explorar sus conexiones','Selecciona una idea para leer qué aporta y cómo se relaciona. Las líneas enlazan también las lecturas entre sí.','Leer la página original','Explorar el Atlas completo','Trabajar con tu asistente','Copia la entrada y dásela a tu asistente. Puedes pedirle una explicación, una comparación o una aplicación a tu pregunta.','Copiar la pregunta y la entrada','Abrir la entrada para tu asistente','Lecturas conectadas','Fuente de esta lectura'),
   'en'=>array('Ideas in conversation with this page','An entrance to the thought Atlas','The Atlas connects pages, ideas, experiences and sources. This map starts from the current reading and opens a path through its conceptual neighbours.','Open the map and explore its connections','Select an idea to read what it contributes and how it connects. Lines also connect the readings with each other.','Read the original page','Explore the complete Atlas','Work with your assistant','Copy the entry and give it to your assistant. Ask for an explanation, a comparison or an application to your own question.','Copy the question and entry','Open the entry for your assistant','Connected readings','Source of this reading'),
   'fr'=>array('Les idées en dialogue avec cette page','Une entrée dans l’Atlas de pensée','L’Atlas relie des pages, des idées, des expériences et des sources. Cette carte part de la lecture actuelle et ouvre un parcours parmi ses voisins conceptuels.','Ouvrir la carte et explorer ses liens','Choisissez une idée pour lire son apport et son lien. Les lignes relient également les lectures entre elles.','Lire la page originale','Explorer l’Atlas complet','Travailler avec votre assistant','Copiez l’entrée et donnez-la à votre assistant. Demandez une explication, une comparaison ou une application à votre question.','Copier la question et l’entrée','Ouvrir l’entrée pour votre assistant','Lectures reliées','Source de cette lecture')
  );
  return $all[isset($all[$lang]) ? $lang : 'es'];
 }
 public static function render() {
  if (!self::allowed() || self::$rendered) { return ''; }
  $all = self::data(); if (!is_array($all)) { return ''; }
  self::$rendered = true; $site = self::site(); $key = $site . ':' . get_queried_object_id();
  $known = isset($all['pages'][$key]); $record = $all['pages'][$known ? $key : $all['defaults'][$site]];
  $title = is_singular() ? get_the_title(get_queried_object_id()) : wp_get_document_title();
  $origin = is_singular() ? get_permalink(get_queried_object_id()) : home_url('/');
  if (!$known) { $record['source'] = array('id'=>'page:' . $key, 'title'=>$title, 'url'=>$origin, 'summary'=>'', 'fichas'=>array()); }
  $lang = $record['lang']; $l = self::labels($lang); $ids = $known ? $record['source']['fichas'] : array();
  $position = count($ids) ? $ids[0] : $origin;
  $entry = add_query_arg(array('cluster'=>$site,'alcance'=>'poroso','desde'=>rawurlencode($origin),'page'=>rawurlencode($origin),'posicionamiento'=>rawurlencode($position),'fichas'=>implode(',', $ids)), plugins_url('assistant.txt', __FILE__));
  $atlas = add_query_arg('focus', $position, 'https://dakleyer.github.io/perspective-beyond/') . '#atlas';
  $context = array('key'=>$key,'known'=>$known,'title'=>$title,'url'=>$origin,'cluster'=>$site,'lang'=>$lang,'entry'=>$entry,'atlas'=>$atlas,'registry'=>plugins_url('registry.json', __FILE__));
  $prompt = $lang === 'en' ? 'Open this Atlas entry: ' . $entry . "\n\nHelp me understand “" . $title . '”. Start from this page, connect two or three relevant ideas and explain why the connection helps. Keep links to the original readings. Ask what I want to understand, compare or create.' : ($lang === 'fr' ? 'Ouvrez cette entrée de l’Atlas : ' . $entry . "\n\nAidez-moi à comprendre « " . $title . ' ». Partez de cette page, reliez deux ou trois idées pertinentes et expliquez leur apport. Conservez les liens vers les lectures originales. Demandez ce que je souhaite comprendre, comparer ou créer.' : 'Abre esta entrada del Atlas: ' . $entry . "\n\nAyúdame a comprender «" . $title . '». Parte de esta página, relaciona dos o tres ideas pertinentes y explica qué aporta la conexión. Conserva enlaces a las lecturas originales. Pregúntame qué quiero comprender, comparar o crear.');
  ob_start(); ?>
  <!-- PB-INSTITUTIONAL-ATLAS-V1:START -->
  <section class="pbiv" id="pb-institutional-atlas" aria-labelledby="pbiv-title" data-pbiv-context="<?php echo esc_attr(wp_json_encode($context, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)); ?>">
   <div class="pbiv-cover"><div><p class="pbiv-kicker">Perspective Beyond <span>/</span> <?php echo esc_html($l[1]); ?></p><h2 id="pbiv-title"><?php echo esc_html($l[0]); ?></h2><p class="pbiv-origin"><?php echo esc_html($title); ?></p></div>
   <svg class="pbiv-emblem" viewBox="0 0 260 150" aria-hidden="true"><g fill="none" stroke="#d3b27b" opacity=".8"><path d="M130 75 65 32 25 75 65 120 130 75 195 30 235 75 195 120 130 75M65 32 195 30M65 120 195 120M65 32 65 120M195 30 195 120M25 75 235 75"/></g><g fill="#e3c591"><circle cx="130" cy="75" r="10"/><circle cx="65" cy="32" r="5"/><circle cx="65" cy="120" r="5"/><circle cx="195" cy="30" r="5"/><circle cx="195" cy="120" r="5"/></g><g fill="#bdd5c9"><circle cx="25" cy="75" r="4"/><circle cx="235" cy="75" r="4"/></g></svg></div>
   <details class="pbiv-main"><summary><span><?php echo esc_html($l[3]); ?></span><span class="pbiv-plus" aria-hidden="true">+</span></summary><div class="pbiv-body"><p class="pbiv-intro"><?php echo esc_html($l[2]); ?></p><p class="pbiv-guide"><?php echo esc_html($l[4]); ?></p>
    <div class="pbiv-map" data-pbiv-map></div><div class="pbiv-mobile" data-pbiv-mobile></div><div class="pbiv-selection" data-pbiv-selection aria-live="polite"></div>
    <noscript><h3><?php echo esc_html($l[11]); ?></h3><ul><?php foreach ($record['nodes'] as $node) { ?><li><a href="<?php echo esc_url($node['url']); ?>"><?php echo esc_html($node['title']); ?></a><p><?php echo esc_html($node['summary']); ?></p></li><?php } ?></ul></noscript>
    <div class="pbiv-actions"><a href="<?php echo esc_url($origin); ?>"><?php echo esc_html($l[5]); ?> ↗</a><a href="<?php echo esc_url($atlas); ?>"><?php echo esc_html($l[6]); ?> ↗</a></div>
    <details class="pbiv-help"><summary><?php echo esc_html($l[7]); ?></summary><p><?php echo esc_html($l[8]); ?></p><textarea class="pbiv-prompt" readonly aria-label="<?php echo esc_attr($l[7]); ?>"><?php echo esc_textarea($prompt); ?></textarea><div class="pbiv-actions"><button type="button" data-pbiv-copy><?php echo esc_html($l[9]); ?></button><a href="<?php echo esc_url($entry); ?>"><?php echo esc_html($l[10]); ?> ↗</a></div><p data-pbiv-copy-status role="status"></p></details>
   </div></details>
  </section>
  <!-- PB-INSTITUTIONAL-ATLAS-V1:END -->
  <?php return ob_get_clean();
 }
 public static function content($content) { if (self::allowed() && is_singular() && in_the_loop() && is_main_query()) { return $content . self::render(); } return $content; }
 public static function footer() { echo self::render(); }
}
add_action('wp_enqueue_scripts', array('PB_Institutional_Visual_Entries_V13','assets'));
add_filter('the_content', array('PB_Institutional_Visual_Entries_V13','content'), 99);
add_action('wp_footer', array('PB_Institutional_Visual_Entries_V13','footer'), 5);
