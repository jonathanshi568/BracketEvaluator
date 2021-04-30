$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (taskID === 'New Task') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Task ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#search-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (taskID === 'Search') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display2').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Task ' + taskID)
            $('#task-form-display2').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-t1id').val(content);
        } else {
            modal.find('.form-t1id').val('');
        }
    })

    $('#submit-task').click(function () {
        const tID = $('#task-form-display').attr('taskID');
        console.log($('#task-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url: tID ? '/matches/edit/' + tID : '/matches/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                't1id': $('#task-modal').find('.form-t1id').val(),
                't2id': $('#task-modal').find('.form-t2id').val(),
                't1score': $('#task-modal').find('.form-control').val(),
                't2score': $('#task-modal').find('.form-t1score').val()
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

    $('#submit-search').click(function () {
        const key = $('#search-modal').find('.form-t1id').val()
        console.log("hi")
        console.log($('#search-modal').find('.form-t1id').val())
        console.log("hi2")
        $.ajax({
            type: 'POST',
            url: '/matches/search/' + key,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'keyword': $('#search-modal').find('.form-t1id').val(),
            }),
            success: function (res) {
                console.log(res.response)
                console.log(this.url)
                location.assign(this.url);
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
            url: '/matches/delete/' + remove.data('source'),
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
        const new_state = null;
        if (state.text() === "In Progress") {
            new_state = "Complete"
        } else if (state.text() === "Complete") {
            new_state = "Todo"
        } else if (state.text() === "Todo") {
            new_state = "In Progress"
        }

        $.ajax({
            type: 'POST',
            url: '/matches/edit/' + tID,
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

    $('#advq').click(function() {
        $.ajax({
            type: 'POST',
            url: '/wldiff',
            contentType: 'application/json;charset=UTF-8',
            success: function (res) {
                console.log(res.response);
                location.assign(this.url);
            },
            error: function() {
                console.log('Error');
            }
        });
    });

});