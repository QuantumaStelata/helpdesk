
$(document).ready(() => {
    if (typeof branch_id === "undefined") {
        throw Error("branch_id not find")
    }

    $('#tree').jstree({
        core : { 'data' : addToTree },
        contextmenu: {
            items: contextMenu
        },
        types: {
            "field": { "icon" : "fa fa-indent text-success" },
            "field-not-active": { "icon" : "fa fa-list-alt text-secondary" },
            "node": { "icon" : "fa fa-code-fork text-primary" },
            "node-not-active": { "icon" : "fa fa-code-fork text-secondary" },
            "edit": { "icon": "fa-solid fa-pen text-warning" },
            "add": { "icon" : "fa fa-plus text-success" },
            "default": { "icon": "fa fa-sliders text-muted" },
        },
        plugins: ["types", "contextmenu"]
    })
})

function contextMenu(node) {
    if (!branch_id) { return }

    return {
        update: {
            label: "Редагувати",
            action: updateObject(node)
        },
        add_childs: {
            label: "Додати " + (node.type.includes("field") ? "ноду" : "поле"),
            action: addObject(node)
        },
        delete: {
            label: "Видалити",
            action: deleteObject(node),
            separator_before: true
        },
        other: {
            label: "Інше",
            separator_before: true,
            submenu: {
                get_branch: {
                    label: "Перейти до гілки",
                    action: goToBranch(node)
                },
                copy: {
                    label: "Копіювати",
                    _disabled: true,
                },
                paste: {
                    label: "Вставити",
                    _disabled: true,
                },
            }
        }
    }
}

function updateObject(node) {
    return (event) => {
        let url = node.original.type.includes("field") ? 
            `/helpdesk/field-update/${node.original.original_id}/`
        : node.original.type.includes("node") ?
            `/helpdesk/node-update/${node.original.original_id}/`
        : null

        if (!url) { return }

        $("#HelpDeskModalEdit").modal("show")
        $("#HelpDeskModalEdit .modal-title").html("Редагування")
        $("#HelpDeskModalEdit .modal-body").html('')
        $("#HelpDeskModalEdit .modal-footer").html('')

        return $.ajax({
            url: url,
            success: (html) => {
                $("#HelpDeskModalEdit .modal-body").html(html)
                $("#HelpDeskModalEdit form select").select2({
                    width: "100%",
                    placeholder: "Виберіть зі списку"
                })
                formListener()
                $("#HelpDeskModalEdit .modal-footer").html(
                    $("<button/>", {
                        class: "btn btn-sm btn-warning",
                        text: "Зберегти"
                    }).click(function() {
                        let form = $("#HelpDeskModalEdit form")[0]
                        let data = new FormData(form)
                        
                        $.ajax({
                            url: url,
                            data: data,
                            processData: false,
                            contentType: false,
                            method: "POST",
                            success: () => {
                                $("#tree").jstree("refresh")
                                $("#HelpDeskModalEdit").modal('hide')
                            },
                            error: (data) => {
                                $("#HelpDeskModalEdit .modal-body").html(data.responseText)
                                $("#HelpDeskModalEdit form select").select2({
                                    width: "100%",
                                    placeholder: "Виберіть зі списку"
                                })
                                formListener()
                            }
                        })        
                    })
                )
            }
        })
    }   
}

function addObject(node) {    
    return (event) => {
        let url = node.original.type.includes("field") ? 
            `/helpdesk/node-create/`
        : node.original.type.includes("node") ?
            `/helpdesk/field-create/`
        : null

        if (!url) { return }

        $("#HelpDeskModalEdit").modal("show")
        $("#HelpDeskModalEdit .modal-title").html("Створення")
        $("#HelpDeskModalEdit .modal-body").html('')
        $("#HelpDeskModalEdit .modal-footer").html('')

        return $.ajax({
            url: url,
            data: {
                parent: node.original.original_id,
                branch: branch_id
            },
            success: (html) => {
                $("#HelpDeskModalEdit .modal-body").html(html)
                $("#HelpDeskModalEdit form select").select2({
                    width: "100%",
                    placeholder: "Виберіть зі списку"
                })
                formListener()
                $("#HelpDeskModalEdit .modal-footer").html(
                    $("<button/>", {
                        class: "btn btn-sm btn-warning",
                        text: "Зберегти"
                    }).click(function() {
                        let form = $("#HelpDeskModalEdit form")[0]
                        let data = new FormData(form)
                        
                        $.ajax({
                            url: url,
                            data: data,
                            processData: false,
                            contentType: false,
                            method: "POST",
                            success: () => {
                                $("#tree").jstree("refresh")
                                $("#HelpDeskModalEdit").modal('hide')
                            },
                            error: (data) => {
                                $("#HelpDeskModalEdit .modal-body").html(data.responseText)
                                $("#HelpDeskModalEdit form select").select2({
                                    width: "100%",
                                    placeholder: "Виберіть зі списку"
                                })
                                formListener()
                            }
                        })        
                    })
                )
            }
        })
    }   
}

function deleteObject(node) {
    return (event) => {
        let url = node.original.type.includes("field") ? 
            `/helpdesk/field-delete/${node.original.original_id}/`
        : node.original.type.includes("node") ?
            `/helpdesk/node-delete/${node.original.original_id}/`
        : null

        if (!url) { return }

        $("#HelpDeskModalEdit").modal("show")
        $("#HelpDeskModalEdit .modal-title").html("Видалення")
        $("#HelpDeskModalEdit .modal-body").html('Ви впевнені, що хочете видалити об\'єкт?')
        $("#HelpDeskModalEdit .modal-footer").html(
            $("<button/>", {
                text: "Так",
                class: "btn btn-sm btn-danger"
            }).click(() => {
                return $.ajax({
                    url: url,
                    method: "POST",
                    success: () => {
                        $("#tree").jstree("refresh")
                        $("#HelpDeskModalEdit").modal("hide")
                    }
                })
            })
        )
    }   
}

function goToBranch(node) {
    return (event) => {
        window.location.href = `/helpdesk/branch-detail/${branch_id}/?start-${node.type.includes('field') ? "field" : "node"}=${node.original.original_id}`
    }
}

function getField(id) {
    let data = {}

    if (branch_id) {
        data = {branch_id}
    }

    return $.ajax({
        url: id ? `/api/fields/${id}/` : "/api/fields/",
        data: data,
        success: function(data) {
            data.text = data.label
            data.field_type = data.type
            data.type = "field"
            data.children = !!data.childs?.length
            data.original_id = data.id
            data.id = (Math.random() + 1).toString(36).substring(7)
        }
    })
}

function getNode(id) {
    return $.ajax({
        url: `/api/nodes/${id}/`,
        success: function(data) {
            data.children = !!data.childs?.length
            data.type = data.is_active ? "node" : "node-not-active"
            data.original_id = data.id
            data.id = (Math.random() + 1).toString(36).substring(7)
        }
    })
}

function addToTree(node, cb) {
    let params = new URLSearchParams(window.location.search)

    let start_with_field = params.get("start-field")
    let start_with_node = params.get("start-node")

    if (node.id === '#') {
        if (start_with_field) {
            return getField(start_with_field).then((node) => cb(node))
        } else if (start_with_node) {
            return getNode(start_with_node).then((node) => cb(node))
        } else {
            return getField().then((node) => cb(node))
        }
        
    } else if (node.original?.label) {
        let promises = []

        for (let _node of node.original.childs) {
            promises.push(getNode(_node.id))
        }

        return Promise.all(promises).then((nodes) => {
            if (node.original.type.includes("not-active")) {
                for (let _node of nodes) {
                    _node.type += "-not-active"
                }
            }
            return cb(nodes)
        })
        
    } else if (node.original?.value) {
        let promises = []

        for (let id of node.original.childs) {
            promises.push(getField(id))
        }
        
        return Promise.all(promises).then((nodes) => {
            if (node.original.type.includes("not-active")) {
                for (let _node of nodes) {
                    _node.type += "-not-active"
                }
            }
            return cb(nodes)
        })
    }
}

function formListener() {
    $("#id_type").change(function() {
        $("#id_label").attr("readonly", false)
        $("#id_help_text").attr("readonly", false)
        $("#id_placeholder").attr("readonly", false)
        $("#id_initial").attr("readonly", false)
        $("#id_min_length").attr("readonly", false)
        $("#id_max_length").attr("readonly", false)

        if (this.value === "select") {
            $("#id_initial, #id_min_length, #id_max_length").attr("readonly", true)
        } else if (this.value === "radio" || this.value === "checkbox") {
            $("#id_placeholder, #id_initial, #id_min_length, #id_max_length").attr("readonly", true)
        } else if (this.value === "image" || this.value === "file") {
            $("#id_placeholder, #id_initial").attr("readonly", true)
        } else if (this.value === "date" || this.value === "time" || this.value === "datetime") {
            $("#id_placeholder, #id_initial, #id_min_length, #id_max_length").attr("readonly", true)
        }
    })

    $("#id_type").change()
}
