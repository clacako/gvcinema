let spinner         = "<div class='spinner-grow text-primary m-1' role='status'><span class='sr-only'>Loading...</span></div>"

// Function active menu
function activeMenu() {
    let path    = window.location.pathname.split("/")

    path.forEach(element => {
        if (element !== "") {
            let div_id  = document.getElementById(element)
            div_id.classList.add("text-success")
        }
    });

}

// Alert message
function alert_message(type, title, message, extra_message="") {
    let result  = "<div class='alert alert-dismissible fade show mb-xl-0 mt-4 alert-" + type + "' role='alert'> <strong>" + title + "</strong> <br />" + message + " " + extra_message + " <button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button> </div>"

    // let result = "<div class='card'> <div class='card-header text-strong text-white bg-" + type +  "'>"  + title + " </div>  <div class='card-body'>  <p class='card-text text-center'>" + message + "</p> </div> </div>"
    return result;
}

// Show message
function showMessage(message, type, mesage_div_id) {
    color   = type == "success" ? "success" : "danger"
    icon    = type == "success" ? "fa fa-check" : "fa fa-exclamation-triangle"

    for (const [key, value] of Object.entries(message)) {
        $(`<div class="alert alert-dismissible fade show mb-xl-0 mt-2 alert-borderless alert-${color}" role="alert">
            <strong> 
                ${key}! <br />
                ${value[0]}
            </strong>
            <button type='button' class='btn-close btn-close-white' data-bs-dismiss='alert' aria-label='Close'></button>
        </div>`).appendTo($(mesage_div_id).parent())
    };
}

// Ajax get by selected id
let xselected   = (div_id, success_function) => {
    let selectedID  = document.getElementById(div_id)

    selectedID.addEventListener("change", function() {
        let value   = selectedID.value
        success_function(value)
    })
}

// Ajax post
let xpost  = (form_id, namespace, success_function) => {
    $("#" + form_id).submit(function(e) {
        e.preventDefault();
        let data = $("#" + form_id).serializeArray();
        $(':input[type="submit"]').prop('disabled', true);
        $.ajax({
            url         : namespace,
            type        : "POST",
            data        : data,
            dataType    : "JSON",
            beforeSend  : function() {
                $(".btn-action").prop("disabled", true);
                $("#loading").addClass("spinner-border")
            },
            success     : function(response) {
                success_function(response)
                $(':input[type="submit"]').prop('disabled', false)
                $("#loading").removeClass("spinner-border")
            },
            error       : ""
        })
    })
}

// Ajax get
let xget  = (form_id, namespace, success_function) => {
    $("#" + form_id).submit(function(e) {
        e.preventDefault()
        let data = $("#" + form_id).serializeArray()
        $.ajax({
            url         : namespace,
            type        : "POST",
            data        : data,
            dataType    : "JSON",
            success     : function(response) {
                success_function(response)
            }
        })
    })
}

// Ajax file
let xupload = (form_id, namespace, success_function) => {
    $("#" + form_id).submit(function(e) {
        e.preventDefault();
        let data = new FormData($("#" + form_id)[0]);
        $(':input[type="submit"]').prop('disabled', true);
        $.ajax({
            url         : namespace,
            type        : "POST",
            data        : data,
            dataType    : "JSON",
            contentType : false,
            processData : false,
            success     : function(response) {
                success_function(response)
                $(':input[type="submit"]').prop('disabled', false)
            }
        })
    })
}

/** 
 * Modal custom function
 * 
*/

// Show modal
let modal_show  = (modal_id, modal_size, modal_body_id, namespace) => {
    size_list   = ["modal-fullscreen", "modal-xl", "modal-lg", "modal-sm"]
    size_list.forEach(size => {
        if ($(".modal-dialog").hasClass(size)) {
            $(".modal-dialog").removeClass(size)
        }
    });

    $(".modal-dialog").addClass(modal_size)

    url = namespace
    $("#" + modal_id).modal("show")
    $.ajax({
        url     : url,
        type    : "GET",
        success : function(response) {
            $("#" + modal_body_id).html(response)
        }
    })
}

// Hide modal
let modal_hide  = (modal_id) => {
    $('#' + modal_id).modal('hide')
}

/** 
 * Touchspin custom function
 * 
*/

let prefix_touchspin    = (input_name) => {
    $("input[name='" + input_name + "']").TouchSpin({
        min             : 0,
        max             : 9999999999999999,
        boostat         : 5,
        maxboostedstep  : 10,
        prefix          : ''
    });
}

/**
 * Offcanvas custom function
 * 
 */

// Offcanvas toggle
// let offcanvas_toggle    = (offcanvas_id, namespace) => {
//     $("#" + offcanvas_id).offcanvas("toggle")
//     url = namespace
//     $.ajax({
//         url     : url,
//         type    : "GET",
//         success : function(response) {
//             $("#offcanvas-response").html(response)
//         }
//     })
// }

// data-bs-toggle  = "dropdown"
// aria-expanded   = "false"

let offcanvas_toggle  = (identifier, title) => {
    let url     = $(identifier).data("namespace")
    
    $("#offcanvasRight").offcanvas("toggle")
    $("#offcanvasRightLabel").html(title)
    $.ajax({
        url     : url,
        type    : "GET",
        success : function(response) {
            $("#offcanvas-response").html(response)
        }
    })
}

/**
 * Update function at Feb 6, 2023 by _claudiocanigia
 * Create a new function onclick event at attribute html
 * 
 */

let load_page   = (identifier) => {
    let namespace   = $(identifier).data("namespace")
    let id_response = $(identifier).data("id-response")
    console.log("Loaded!")
    $.ajax({
        url         : namespace,
        type        : "GET",
        // beforeSend  : function() {
        //     $("#" + div_id).html(spinner)
        // },
        success     : function(response) {
            $(id_response).html(response)
        }
    })
}

let loadPageByID    = (identifier, id_resp="", namespace="", csnamespace) => {
    let id_div, url, id_res

    if (typeof(identifier) === "object") {
        namespace   = $(identifier).data("namespace")
        csnamespace = $(identifier).data("csnamespace")
        id_div      = identifier.id
        url         = typeof(namespace) !== "undefined" ? namespace : `${csnamespace}/${id_div}`
        id_res      = $(identifier).data("id-resp")
    } else {
        id_div  = identifier
        url     = namespace != "" ? namespace : `${csnamespace}/{id_div}`
        id_res = id_resp
    }
    
    $.ajax({
        url         : url,
        type        : "GET",
        // beforeSend  : function() {
        //     $("#" + div_id).html(spinner)
        // },
        success     : function(response) {
            $("#" + id_res).html(response)
        }
    })

    // let selectedID  = document.getElementById(identifier.id)
    // console.log(typeof(identifier))
    
    // selectedID.addEventListener("change", function() {
    //     let value   = selectedID.value
    //     success_function(value)
    // })
}

let show_modal  = (identifier, title) => {
    let namespace   = $(identifier).data("namespace")
    let modal_size  = $(identifier).data("modal-size")
    
    size_list   = ["modal-fullscreen", "modal-xl", "modal-lg", "modal-sm"]
    size_list.forEach(size => {
        if ($(".modal-dialog").hasClass(size)) {
            $(".modal-dialog").removeClass(size)
        }
    });

    $(".modal-dialog").addClass(modal_size)
    $("#modal-title").html(title)
    $("#show-modal").modal("show")
    $.ajax({
        url     : namespace,
        type    : "GET",
        success : function(response) {
            $("#response").html(response)
        }
    })
}

// Ajax unload
let ajx_unload = (div_id)=> {
    $("#" + div_id).unbind("click")
    console.log("Unloaded!")
    $("#" + div_id).empty()
}

let ajx_load   = (div_id, namespace) => {
    ajx_unload(div_id)
    console.log("Loaded!")
    $.ajax({
        url         : namespace,
        type        : "GET",
        // beforeSend  : function() {
        //     $("#" + div_id).html(spinner)
        // },
        success     : function(response) {
            $("#" + div_id).html(response)
        }
    })
}