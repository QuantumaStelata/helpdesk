class Field {
    constructor(field) {
        if (this.constructor.name === Field.name) {
            throw new Error(`Class ${this.constructor.name} is mixin class`)
        }

        if (this.constructor.name !== Field.name && typeof this.create_field !== "function") {
            throw new Error(`Class ${this.constructor.name} hasn't method 'create_field'`)
        }

        Object.assign(this, field)

        this.field_id = `helpdesk-field-${this.id}`
        this.field_name = "helpdesk-field"
    }

    get_label() {
        return $("<label/>", {
            text: this.label
        })
    }

    get_help_text() {
        return $("<small/>", {
            text: this.help_text,
            class: "text-muted"
        })
    }

    get_field() {
        return this.field ? this.field : function (that) {
            that.field = that.create_field()
            return that.field
        }(this)
    }

    get_searchparam() {
        return new URLSearchParams(window.location.search).get(this.field_id)
    }

    add_field($container) {
        $container.append(
            $("<div/>", {
                class: "d-flex flex-column mb-2"
            }).append(
                this.get_label(), 
                this.get_field(),
                this.get_help_text()
            )
        )
    }
}


class Select extends Field {
    add_field($container) {
        super.add_field($container)

        this.get_field().select2({
            placeholder: this.placeholder || "Выбери из списка",
            allowClear: true
        })
    }

    create_field() {
        return $("<select/>", {
            id: this.field_id,
            name: this.field_name
        }).append(this.get_choices())
    }

    get_choices() {
        return [$("<option/>"), ...Array.from(this.childs, choice => choice.is_active ? $("<option/>", {
            text: choice.text,
            value: choice.value,
            selected: (this.get_searchparam() || this.initial) === choice.value 
        }) : null)]
    }
}


class Text extends Field {
    create_field() {
        return $("<textarea/>", {
            class: "form-control",
            rows: 3,
            placeholder: this.placeholder,
            id: this.field_id,
            name: this.field_name,
            "minlength": this.min_length || null,
            "maxlength": this.max_length || null,
        }).html(this.get_searchparam() || this.initial)
    }
}


class Radio extends Field {
    create_field() {
        return Array.from(this.childs, choice => 
            $("<div/>", {
                class: "d-flex flex-row align-items-center"
            }).append(
                $("<input/>", {
                    type: "radio",
                    role: "button",
                    id: `${this.field_id}-${choice.value}`,
                    name: this.field_id,
                    value: choice.value,
                    checked: (this.get_searchparam() || this.initial) == choice.value
                })
            ).append(
                $("<label/>", {
                    class: "m-0 ml-2",
                    role: "button",
                    text: choice.text,
                    for: `${this.field_id}-${choice.value}`
                })
            )
        )
    }
}


class Number extends Field {
    create_field() {
        return $("<input/>", {
            class: "form-control",
            type: "number",
            placeholder: this.placeholder,
            id: this.field_id,
            "min": this.min_length || null,
            "max": this.max_length || null,
        }).html(this.get_searchparam() || this.initial)
    }
}