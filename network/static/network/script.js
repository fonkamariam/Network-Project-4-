
  function Save(h){
    a=document.getElementById(`${h}`)
    c=document.getElementById(`2${h}`)
    b=document.getElementById(`1${h}`)
    all=document.getElementById(`3${h}`)
    b=b.value
    fetch(`/edit/${h}`, {
      method: 'PUT',
      body: JSON.stringify({
          text: b
      })
    })
    a.innerHTML=b
    a.style.fontWeight='bold';
    a.style.display='block';
    all.style.display='none';
    d.style.display='block';
  }
  function Edit(h){
    a=document.getElementById(`${h}`)//text
    b=document.getElementById(`1${h}`)//textarea
    c=document.getElementById(`2${h}`)//save
    d=document.getElementById(`4${h}`)
    all=document.getElementById(`3${h}`)
    a.style.display='none';
    d.style.display='none';
    all.style.display='block';
    
  }
    const btnlike = document.getElementById('bt1');
     function Toggle(){
      console.log(btnlike.id)
      if(btnlike.fill == "white"){
        btnlike.fill == "red"
      }else{
        btnlike.fill == "white"
      }
     }
      
    document.addEventListener('DOMContentLoaded', function() {
      const text= document.getElementById("post")
           const submitt= document.getElementById("submitbutton")
           text.addEventListener('keyup',(e)=>{
               const value= e.currentTarget.value;
               let result= value.trim();
               if ( result == "" ){
                   submitt.disabled=true;
               }else{
                   submitt.disabled=false;
               }
           });
     
     });

