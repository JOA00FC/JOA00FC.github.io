'use strict';
(() => {
  const canvas = document.querySelector('#preview');
  const ctx = canvas.getContext('2d', {willReadFrequently:true, colorSpace:'srgb'});
  const status = document.querySelector('#preview-status');
  const label = document.querySelector('#preview-label');
  const file = document.querySelector('#photo');
  const buttons = [...document.querySelectorAll('[data-look]')];
  let base, look='original', custom=false, request=0;
  const note='Prévia da transformação de cor das LUTs, sem granulação ou vinheta. Não simula o renderizador do Lightroom.';
  const tone = (x, mono=false) => (mono?.015:.018)+(mono?.970:.960)*(x-(mono?.035:.025)*Math.sin(2*Math.PI*x));
  function render() {
    const output=new ImageData(new Uint8ClampedArray(base.data), base.width, base.height);
    const d=output.data;
    if(look!=='original') for(let i=0;i<d.length;i+=4){
      let r=d[i]/255,g=d[i+1]/255,b=d[i+2]/255;
      if(look==='mono') { r=g=b=tone(.28*r+.62*g+.10*b,true); }
      else {
        r=tone(r);g=tone(g);b=tone(b);
        const y=.2126*r+.7152*g+.0722*b,w=4*y*(1-y);
        r=y+.88*(r-y)+.014*w;g=y+.88*(g-y)+.003*w;b=y+.88*(b-y)-.011*w;
      }
      d[i]=r*255;d[i+1]=g*255;d[i+2]=b*255;
    }
    ctx.putImageData(output,0,0);
    label.textContent=(custom?'Sua foto':'Cartela de cores')+' · '+({original:'original',color:'Color Soft',mono:'Mono Soft'}[look]);
    for(const b of buttons) b.setAttribute('aria-pressed',String(b.dataset.look===look));
  }
  function chart(){
    custom=false;canvas.width=1000;canvas.height=600;
    const swatches=['#bd9178','#805a44','#49372d','#d2c2a3','#e4cfb6','#546e60','#687e92','#b5503d','#d0ad59','#797585'];
    const ramp=ctx.createLinearGradient(0,0,1000,0);ramp.addColorStop(0,'#080808');ramp.addColorStop(1,'#fafafa');
    ctx.fillStyle=ramp;ctx.fillRect(0,0,1000,190);
    swatches.forEach((c,i)=>{ctx.fillStyle=c;ctx.fillRect(i%5*200,190+Math.floor(i/5)*205,200,205)});
    base=ctx.getImageData(0,0,1000,600);render();status.textContent=note;
  }
  buttons.forEach(b=>b.addEventListener('click',()=>{look=b.dataset.look;render()}));
  document.querySelector('#reset').addEventListener('click',()=>{request++;file.value='';look='original';chart()});
  file.addEventListener('change',async()=>{
    const f=file.files[0];if(!f)return;
    const token=++request;
    if(f.size>40*1024*1024){status.textContent='Escolha uma foto JPG, PNG ou WebP de até 40 MB.';return}
    status.textContent='Abrindo foto no seu navegador…';
    try{
      const bitmap=await createImageBitmap(f);
      if(token!==request){bitmap.close();return}
      const scale=Math.min(1,1400/Math.max(bitmap.width,bitmap.height));
      canvas.width=Math.max(1,Math.round(bitmap.width*scale));canvas.height=Math.max(1,Math.round(bitmap.height*scale));
      ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);
      ctx.drawImage(bitmap,0,0,canvas.width,canvas.height);bitmap.close();
      base=ctx.getImageData(0,0,canvas.width,canvas.height);custom=true;render();status.textContent=note;
    }catch(error){status.textContent='Não foi possível abrir esta imagem. Experimente uma foto JPG, PNG ou WebP em SDR.'}
  });
  chart();
})();
