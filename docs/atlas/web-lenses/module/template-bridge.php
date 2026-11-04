<?php
/**
 * Plugin Name: Mind Atlas — custom template bridge
 * Description: Connects home pages and timelines using a custom template to the same Mind Atlas.
 * Version: 1.0.0
 */
if(!defined('ABSPATH'))exit;
add_action('init',function(){
 if(is_admin()||wp_doing_ajax()||defined('REST_REQUEST')&&REST_REQUEST)return;
 $host=strtolower((string)wp_parse_url(home_url('/'),PHP_URL_HOST));if(!in_array($host,array('jubap.net','jubap.us'),true))return;
 $path=rtrim((string)wp_parse_url($_SERVER['REQUEST_URI'],PHP_URL_PATH),'/');if(!in_array($path,array('','/case-studies'),true))return;
 ob_start(function($html)use($host,$path){
  if(strpos($html,'id="pbmind-context"')!==false||stripos($html,'</body>')===false)return $html;
  $site=$host==='jubap.net'?'net':'us';$id=$path===''?2:250;$url=home_url($path===''?'/':$path.'/');$context=array('key'=>$site.':'.$id,'url'=>$url,'title'=>get_the_title($id),'site'=>$site,'lang'=>'en');
  $assets=home_url('/wp-content/plugins/mind-atlas-page-windows/');
  $extra='<script type="application/json" id="pbmind-context">'.wp_json_encode($context,JSON_HEX_TAG|JSON_HEX_AMP|JSON_HEX_APOS|JSON_HEX_QUOT).'</script><div id="pbmind-fallback" hidden><aside class="pbx"><div class="pbx-cover"><div class="pbx-copy"><p class="pbx-kicker">Perspective Beyond / Mind Atlas</p><h2>'.esc_html(get_the_title($id)).'</h2><a class="pbx-atlas" href="https://integralmanagement.ch/nueva-perspectiva/atlas-mental/?pagina='.$site.'%3A'.$id.'">Explore this reading in Mind Atlas ↗</a></div></div><details class="pbx-details"><summary>Map of ideas and connections <span class="pbx-count"></span></summary><div class="pbx-branches"></div></details></aside></div><link rel="stylesheet" href="'.esc_url($assets.'web.css?v=template-1').'"><script src="'.esc_url($assets.'web.js?v=template-1').'"></script><!-- MIND-ATLAS-TEMPLATE-ENTRY -->';
  return preg_replace('/<\/body\s*>/i',$extra.'</body>',$html,1);
 });
},-999);
