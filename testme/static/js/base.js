function showSuccessMessage(success, successSelector, errorSelector, timeout, postHandler) {
    successSelector = successSelector ? successSelector : '.success';
    errorSelector = errorSelector ? errorSelector : '.error';
    $(errorSelector).html('');
    $(errorSelector).hide();
    $(successSelector).html(success);
    $(successSelector).show();
    if (timeout) {
        setTimeout(function(){
            clearMessages(successSelector, errorSelector);
            if (postHandler){
                postHandler();
            }
        }, timeout);
    }
}

function showErrorMessage(error, successSelector, errorSelector) {
    successSelector = successSelector ? successSelector : '.success';
    errorSelector = errorSelector ? errorSelector : '.error';
    $(successSelector).html('');
    $(successSelector).hide();
    $(errorSelector).html(error);
    $(errorSelector).show();
}

function clearMessages(successSelector, errorSelector) {
    successSelector = successSelector ? successSelector : '.success';
    errorSelector = errorSelector ? errorSelector : '.error';
    successSelector = $('.success');
    errorSelector = $('.error');
    $(successSelector).html('');
    $(successSelector).hide();
    $(errorSelector).html('');
    $(errorSelector).hide();
}


function getFormData($form){
    var raw_arr = $form.serializeArray();
    var arr = {};
    $.map(raw_arr, function(n, i){
        arr[n['name']] = n['value'];
    });
    return arr;
}


function preErrorHandle(xhr, exception) {
    var error = false;
    if(xhr.status === 403) {
        var content = $($.parseHTML(xhr.responseText.trim())).filter('main');
        $('body').html($(content));
        error = true;
    } else if (xhr.status === 401) {
        window.location.href = '/login';
        error = true;
    }
    return error;
}


/**
 *  Call this handler within the error method of ajax request.
 * @param {*} xhr
 * @param {*} exception
 */
function ajaxErrorHandler(xhr, exception, errorHandle, modal) {
    if(xhr.status !== 403 && xhr.status !== 401) {
        errorHandle();
    } else {
        if(modal) {
            $(modal).hide();
        }
        preErrorHandle(xhr, exception);
    }
}


/** do ajax request */
function doAjaxRequest(me, url, data, method, success, error, modal, postHandler) {
    // show spinner
    $($(me).find('.nonSpinnerText')[0]).hide();
    $($(me).find('.spinnerText')[0]).show();

    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function (result) {
            if(postHandler) {
                postHandler(result);
            } else {
                showSuccessMessage("Successfully.", success, error, 500, function () {
                    if(modal) {
                        $(modal).hide()
                    }
                    window.location.reload();
                });
            }
        },
        error: function (jqXHR, exception) {
            // hide spinner
            $($(me).find('.spinnerText')[0]).hide();
            $($(me).find('.nonSpinnerText')[0]).show();

            ajaxErrorHandler(jqXHR, exception, function() {
                var res = JSON.parse(jqXHR.responseText);
                showErrorMessage(res['message'], success, error);
            }, modal);
        }
    });
}

function doCreationRequest(me, url, data, modal, postHandler) {
    doAjaxRequest(me, url, data, 'POST', '.success-creation', '.error-creation', modal, postHandler);
}

function doUpdateRequest(me, url, data, modal, postHandler) {
    doAjaxRequest(me, url, data, 'PUT', '.success-update', '.error-update', modal, postHandler);
}

function doDeletionRequest (me, url, data, modal, postHandler) {
    doAjaxRequest(me, url, data, 'DELETE', '.success-deletion', '.error-deletion', modal, postHandler);
}


/** file upload request. */
function doUploadFile(me, url, data, success, error, modal) {
    // show spinner
    $($(me).find('.nonSpinnerText')[0]).hide();
    $($(me).find('.spinnerText')[0]).show();

    $.ajax({
        url: url,
        type: 'post',
        data: data,
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: false,
        success: function (result) {
            showSuccessMessage("Successfully.", success, error, 500, function(){
                if(modal) {
                    $(modal).hide()
                }
                window.location.reload();
            });
        },
        error: function (jqXHR, exception) {
            $($(me).find('.spinnerText')[0]).hide();
            $($(me).find('.nonSpinnerText')[0]).show();
            ajaxErrorHandler(jqXHR, exception, function() {
                var res = JSON.parse(jqXHR.responseText);
                showErrorMessage(res['message'], success, error);
            }, modal);
        }
    });
}
