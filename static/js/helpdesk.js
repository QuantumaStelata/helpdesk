$("#HelpDeskModal").on('show.bs.modal', function () {
    $("#HelpDeskModal .modal-title").html("HelpDesk")
    $("#HelpDeskModal .modal-body").html("")
    const urlParams = new URLSearchParams(window.location.search)
    const start = urlParams.get("helpdesk-start") || null
    return new HelpDesk(start)
}).on('hidden.bs.modal', function () {
    $("#HelpDeskModal .modal-body").html("")

    const urlParams = new URLSearchParams(window.location.search)
    
    for (let param of Array.from(urlParams.keys())) {
        if (param.startsWith("helpdesk"))  {
            urlParams.delete(param)
        }
    }
    
    window.history.replaceState({}, null, urlParams.toString() ? "?" + urlParams.toString() : window.location.pathname)
})

$(document).ready(() => {
    const urlParams = new URLSearchParams(window.location.search)
    
    for (let param of urlParams.keys()) {
        if (param.startsWith("helpdesk")) { $("#HelpDeskModal").modal("show") }
    }
}) 

class HelpDesk {
    constructor(start_field_id) {
        this.$container = $("#HelpDeskModal .modal-body")
        this.get_field_data(start_field_id).then(data => this.add_field(data))
    }

    get_field_data(id) {
        let url 

        if (id) {
            url = `/api/fields/${id}/`
        } else if (typeof branch_id !== "undefined") {
            url = `/api/fields/?branch_id=${branch_id}`
        } else {
            url = "/api/fields/"
        }

        return $.ajax({ url: url })
    }

    add_field(data) {
        let that = this
        let field

        if (data.type === "select") {
            field = new Select(data)

            field.get_field().on("change", function () {
                let promises = []

                for (let choice of field.childs) {
                    if (choice.value === this.value) {
                        if (choice.childs?.length) {
                            for (let _field of choice.childs) {
                                promises.push(that.get_field_data(_field))
                            }
                        }
                    }
                }

                Promise.all(promises).then(data_array => { 
                    for (let data of data_array) { that.add_field(data) }
                })
            })
        } else if (data.type === "radio") {
            field = new Radio(data)
        } else if (data.type === "number") {
            field = new Number(data)
        } else if (data.type === "text") {
            field = new Text(data)
        } else {
            throw new Error(`Field has no registered class for type '${data.type}'`)
        }

        field.add_field(this.$container)

        field.get_field().on("change", function () {
            $(this).parent().nextAll().remove()

            let $fields = $("[id*=helpdesk-field-]").not("[role=textbox]")
            const urlParams = new URLSearchParams(this.value ? window.location.search : "")

            $fields.each(function () {
                if (!this.value) { return }
                urlParams.set(this.id, this.value)
            });

            window.history.replaceState({}, null, urlParams.toString() ? "?" + urlParams.toString() : window.location.pathname)
        })

        if (field.get_field().val()) {
            field.get_field().change()
        }
    }
}
