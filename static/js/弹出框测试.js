$(function () {
  $('[data-toggle="popover"]').popover({
    container: 'body',

  })
})
const blobToFile = (blob, fileName) => {
             return new File([blob], fileName, {type: blob.type});
        }