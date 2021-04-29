console.log("WTF");

$(document).ready(function () {
  // example: https://getbootstrap.com/docs/4.2/components/modal/
  // show modal
  $('#team-modal').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget) // Button that triggered the modal
    const teamID = button.data('source') // Extract info from data-* attributes
    const content = button.data('content') // Extract info from data-* attributes
    app.logger.info('%s logged in successfully', teamID)
    const modal = $(this)
    if (teamID === 'New Team') {
      modal.find('.modal-title').text(teamID)
      $('#team-form-display').removeAttr('teamID')
    } else {
      modal.find('.modal-title').text('Edit Team ' + teamID)
      $('#team-form-display').attr('teamID', teamID)
    }

    if (content) {
      modal.find('.form-control').val(content);
    } else {
      modal.find('.form-control').val('');
    }
  })


  $('#submit-team').click(function () {
    const tID = $('#team-form-display').attr('teamID');
    console.log($('#team-modal').find('.form-control').val())
    $.ajax({
      type: 'POST',
      url: tID ? '/teams/edit/' + tID : '/teams/create',
      contentType: 'application/json;charset=UTF-8',
      data: JSON.stringify({
        'description': $('#team-modal').find('.form-control').val()
      }),
      success: function (res) {
        console.log(res.response)
        location.reload();
      },
      error: function () {
        console.log('Error');
      }
    });
  });

  $('.remove').click(function () {
    const remove = $(this)
    $.ajax({
      type: 'POST',
      url: '/teams/delete/' + remove.data('source'),
      success: function (res) {
        console.log(res.response)
        location.reload();
      },
      error: function () {
        console.log('Error');
      }
    });
  });

  $('.state').click(function () {
    const state = $(this)
    const tID = state.data('source')
    const new_state
    if (state.text() === "In Progress") {
      new_state = "Complete"
    } else if (state.text() === "Complete") {
      new_state = "Todo"
    } else if (state.text() === "Todo") {
      new_state = "In Progress"
    }

    $.ajax({
      type: 'POST',
      url: '/teams/edit/' + tID,
      contentType: 'application/json;charset=UTF-8',
      data: JSON.stringify({
        'status': new_state
      }),
      success: function (res) {
        console.log(res)
        location.reload();
      },
      error: function () {
        console.log('Error');
      }
    });
  });

});