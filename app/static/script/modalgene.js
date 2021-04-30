$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes
        const userID = button.data('user')

        const modal = $(this)
        if (taskID === 'New Bracket') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Bracket ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
        if (userID) {
            modal.find('.form-user').val(userID);
        } else {
            modal.find('.form-user').val('');
        }
    })


    $('#submit-task').click(function () {
        const tID = $('#task-form-display').attr('taskID');
        console.log($('#task-modal').find('.form-control').val())
        const uID = $('#task-modal').find('.form-user').val()
        console.log(uID)
        $.ajax({
            type: 'POST',
            url: tID ? '/brackets/edit/' + tID : '/brackets/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                "description": $('#task-modal').find('.form-control').val(),
                "user-id":  uID ? + uID: NULL
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
            url: '/brackets/delete/' + remove.data('source'),
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
        const new_state = NULL
        if (state.text() === "In Progress") {
            new_state = "Complete"
        } else if (state.text() === "Complete") {
            new_state = "Todo"
        } else if (state.text() === "Todo") {
            new_state = "In Progress"
        }

        $.ajax({
            type: 'POST',
            url: '/brackets/edit/' + tID,
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


    $('#search-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const id = $('#search-modal').find('.search-word').val()
    })

    $('#search').click(function () {
        const keyword = $('#search-modal').find('.search-word').val()
        console.log(keyword)
        $.ajax({
            type: 'POST',
            url: '/brackets/search/'+ keyword,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'keyword': keyword
            }),
            success: function (res) {
                location.assign(this.url)
                console.log(res.response)
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#winner').click(function () {
        $.ajax({
            type: 'POST',
            url: '/numbracketswinners/',
            contentType: 'application/json;charset=UTF-8',
            success: function (res) {
                location.assign(this.url)
                console.log(res.response)
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});