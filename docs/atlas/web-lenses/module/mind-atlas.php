<?php
/**
 * Plugin Name: Mind Atlas — shared graph windows
 * Description: Reading selections with weights, tokens and connections to Mind Atlas. Preserves page maps and text.
 * Version: 1.0.0
 * License: GPL-2.0-or-later
 */
if (!defined('ABSPATH')) { exit; }
final class PB_Mind_Atlas_Windows {
 private static $done=false;
 private static function site(){ $host=strtolower((string)wp_parse_url(home_url('/'),PHP_URL_HOST));$map=array('jubap.eu'=>'eu','jubap.net'=>'net','jubap.us'=>'us','tegrity.ai'=>'tegrity','integralmanagement.ch'=>'imsv','totonacapan.com'=>'totonacapan');return isset($map[$host])?$map[$host]:''; }
 private static function allowed(){return self::site()&&!is_admin()&&!is_feed()&&!(defined('REST_REQUEST')&&REST_REQUEST);}
 public static function route(){
  if(!self::allowed())return;$path=rtrim((string)wp_parse_url($_SERVER['REQUEST_URI'],PHP_URL_PATH),'/');
  if(!in_array($path,array('/mind-atlas','/nueva-perspectiva/atlas-mental'),true))return;
  status_header(200);header('Content-Type: text/html; charset=UTF-8');$base=plugins_url('/',__FILE__);echo str_replace('__ASSETS__',esc_url($base),(string)file_get_contents(__DIR__.'/mind.html'));exit;
 }
 public static function assets(){if(!self::allowed())return;wp_enqueue_style('pb-mind-atlas-tools',plugins_url('web.css',__FILE__),array(),'1.0.0');wp_enqueue_script('pb-mind-atlas-windows',plugins_url('web.js',__FILE__),array(),'1.0.0',true);}
 public static function render(){
  if(!self::allowed()||self::$done)return '';self::$done=true;$key=self::site().':'.get_queried_object_id();$url=is_singular()?get_permalink(get_queried_object_id()):home_url('/');$title=is_singular()?get_the_title(get_queried_object_id()):wp_get_document_title();$lang='en';$context=array('key'=>$key,'url'=>$url,'title'=>$title,'site'=>self::site(),'lang'=>$lang,'assets'=>plugins_url('/',__FILE__));
  ob_start();?><script type="application/json" id="pbmind-context"><?php echo wp_json_encode($context,JSON_HEX_TAG|JSON_HEX_AMP|JSON_HEX_APOS|JSON_HEX_QUOT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);?></script>
  <div id="pbmind-fallback" hidden><aside class="pbx" id="mind-atlas-page-map" aria-labelledby="mind-atlas-page-title"><div class="pbx-cover"><div class="pbx-copy"><p class="pbx-kicker">◇ Perspective Beyond <span class="pbx-separator">/</span> Mind Atlas</p><h2 id="mind-atlas-page-title"><?php echo esc_html($title);?></h2><p class="pbx-lens"><?php echo $lang==='es'?'Una lectura y sus relaciones dentro del mismo Atlas.':'A reading and its relationships within the same Atlas.';?></p><a class="pbx-atlas" href="https://integralmanagement.ch/nueva-perspectiva/atlas-mental/"><?php echo $lang==='es'?'Explorar esta lectura en el Atlas Mental':'Explore this reading in Mind Atlas';?> ↗</a></div><div class="pbx-art"><svg class="pbx-diagram" viewBox="0 0 280 156" aria-hidden="true"><g fill="none" stroke="#6f9688"><ellipse cx="140" cy="78" rx="118" ry="65"/><ellipse cx="140" cy="78" rx="77" ry="45"/><path d="M25 78h230M140 14v128" opacity=".35"/></g><g fill="none" stroke="#d2ac74"><path d="M140 78 80 48 40 32M80 48 23 63M140 78 80 108 23 93M80 108 40 125M140 78 200 48 240 32M200 48 257 63M140 78 200 108 257 93M200 108 240 125"/></g><g fill="#efd09c"><circle cx="140" cy="78" r="9"/><circle cx="80" cy="48" r="4"/><circle cx="80" cy="108" r="4"/><circle cx="200" cy="48" r="4"/><circle cx="200" cy="108" r="4"/></g></svg></div></div><details class="pbx-details"><summary><span><?php echo $lang==='es'?'Mapa de ideas y conexiones':'Map of ideas and connections';?></span><span class="pbx-count"></span><span class="pbx-toggle" aria-hidden="true"></span></summary><div class="pbx-branches"></div></details></aside></div>
  <!-- MIND-ATLAS-PAGE-WINDOW: <?php echo esc_html($key);?> --><?php return ob_get_clean();
 }
 public static function content($text){return self::allowed()&&is_singular()&&in_the_loop()&&is_main_query()?$text.self::render():$text;}
 public static function footer(){echo self::render();}
}
add_action('template_redirect',array('PB_Mind_Atlas_Windows','route'),0);
add_action('wp_enqueue_scripts',array('PB_Mind_Atlas_Windows','assets'),99);
add_filter('the_content',array('PB_Mind_Atlas_Windows','content'),101);
add_action('wp_footer',array('PB_Mind_Atlas_Windows','footer'),99);
