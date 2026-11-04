// Canonical focus keys shared by the selector and the graph reader.
export function parseFocusWeights(tokens, allowedKeys, limit=20) {
  const keys=[...allowedKeys], known=new Set(keys), folded=new Map();
  for(const key of keys){const k=key.toLowerCase();folded.set(k,folded.has(k)?null:key);}
  const weights=new Map(),errors=[],normalizations=[];
  if(tokens.length>limit)return {weights,errors:['The selection allows up to '+limit+' weights.'],normalizations};
  for(const token of tokens){
    const at=token.lastIndexOf(':'),raw=token.slice(0,at).trim();
    const key=known.has(raw)?raw:folded.get(raw.toLowerCase());
    const value=token.slice(at+1).trim().replace(',','.');
    const number=Number(value);
    if(at<1||!key||!/^\d+(?:\.\d+)?$/.test(value)||!Number.isFinite(number)||number<=0||number>10000){
      errors.push('Review weight “'+token+'”: choose an available tag and a number between 0 and 10000, greater than zero.');continue;
    }
    if(weights.has(key)){errors.push('Tag “'+key+'” appears twice. Retain a single weight.');continue;}
    weights.set(key,number);
    if(key!==raw)normalizations.push({from:raw,to:key});
  }
  return {weights,errors,normalizations};
}
