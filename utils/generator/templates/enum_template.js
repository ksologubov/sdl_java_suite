{% extends "base_template.js" %}
{% block typedef %}
/**
{%- if description %}
 * {{description}}
{%- endif %}
 * @typedef {% raw %}{{% endraw %}{{extend}}{% raw %}}{% endraw %} {{name}}
 * @property {Object} _MAP
 */
{%- endblock %}
{% block body %}
    /**
     * @constructor
     */
    constructor() {
        super();
    }
    {%- for e in methods %}

    /**{% for d in e.description %}
     * {{d}}{%- endfor %}
     * @return {{"%s%s%s"|format("{", e.type, "}")}}
     */
    static get {{e.method_title}}() {
        return {{name}}._MAP.{{e.method_title}};
    }
    {%- endfor %}

    /**
     * Confirms whether the value passed in exists in the Enums of this class
     * @param {String} value
     * @return {null|String} - Returns null if the enum value doesn't exist
     */
    static valueForString(value) {
        return {{name}}.valueForStringInternal(value, {{name}}._MAP);
    }
{% endblock %}
{% block properties %}
{{name}}._MAP = Object.freeze({
{%- for e in params %}
    '{{e.key}}': {{e.value}},
{%- endfor %}
});
{%- endblock %}