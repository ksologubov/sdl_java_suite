{% extends "base_template.js" %}

{% block typedef %}
{%- if description|length %}
/**
 * {{description}}
 */
{%- endif %}
{%- endblock %}
{% block body %}
    /**
     * @constructor
     */
{%- block constructor %}
{% endblock -%}
    {% for e in methods %}
    {% set l = e.type|length + e.last|length + 12 -%}
    /**
     * {% for d in e.description -%}
     {% if loop.index == 1 -%}
     @param {{"%s%s%s %s"|format("{", e.type, "}", e.last)}}  {{d}}
     {% else -%}
     * {{d|indent(l,True)}}
     {% endif -%} {% endfor -%}
     * @return {{"%s%s%s"|format("{", name, "}")}}
     */
    set{{e.upper}}({{e.last}}) {
        {%- if e.type != "Number" and e.type != "Boolean" and "Array" not in e.type %}
        this.validateType({{e.foreign if e.foreign else "String"}}, {{e.last}});
{% endif %}
        {%- if e.foreign %}
        this.setValue({{name}}.KEY_{{e.key}}, {{e.last}});
        {%- else %}
        this.setParameter({{name}}.KEY_{{e.key}}, {{e.last}});
        {%- endif %}
        return this;
    }

    /**
     * @return {{"%s%s%s"|format("{", e.type, "}")}}
     */
    get{{e.upper}}() {
        {%- if e.foreign %}
        return this.getObject({{e.foreign}}, {{name}}.KEY_{{e.key}});
        {%- else %}
        return this.getParameter({{name}}.KEY_{{e.key}});
        {%- endif %}
    }
{% endfor %}
{%- endblock %}
{% block properties %}
{%- for e in params %}
{{name}}.KEY_{{e.key}} = '{{e.value}}';
{%- endfor %}
{%- endblock %}