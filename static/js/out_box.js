$(function () {
  $('[data-toggle="popover"]').popover({
    container: 'body',

  })
})
const blobToFile = (blob, fileName) => {
             return new File([blob], fileName, {type: blob.type});
        }

function modal_show(Current_page) {
    console.log(Current_page)
    if(Current_page==='DOCS' || Current_page==='CONTROL_INDEX'){
        $('#staticBackdrop').modal('show');
        }
    }
function modal_true() {
    var name = $('#id_name').val();
    $.ajax({
        url:'/test',
        data:{name:name},
        complete:function () {
            $('#staticBackdrop').modal('hide');
        }
    })
}


