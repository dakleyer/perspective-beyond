
const q=document.querySelector('#query'),s=document.querySelector('#concept'),o=document.querySelector('#order'),grid=document.querySelector('#cards');
const cards=[...grid.children],norm=t=>t.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function apply(){let n=0;for(const c of cards){c.hidden=!(norm(c.dataset.search).includes(norm(q.value))&&(!s.value||c.dataset.tags.split(' ').includes(s.value)));if(!c.hidden)n++}document.querySelector('#count').textContent=n+' fichas';document.querySelector('#empty').hidden=n>0}
q.addEventListener('input',apply);s.addEventListener('change',apply);o.addEventListener('change',()=>{cards.sort((a,b)=>o.value==='old'?a.id.localeCompare(b.id):b.id.localeCompare(a.id));grid.replaceChildren(...cards)});
function reveal(){let target=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(target&&target.classList.contains('card')){q.value='';s.value='';apply();target.scrollIntoView({block:'start'})}}window.addEventListener('hashchange',reveal);reveal();
