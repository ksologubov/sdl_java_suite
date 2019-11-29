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
    {% if scripts is defined -%}
    {% for s in scripts %}
{{s|indent(4,True)}}
    {% endfor -%}
    {% endif -%}
    {% for e in methods %}
    {% set l = e.type|length + e.param_name|length + 12 -%}
    /**
     {% if not e.description -%}
     * @param_name {{"%s%s%s %s"|format("{", e.type, "}", e.param_name)}}
     {% else -%}
     * {% for d in e.description -%}
     {% if loop.index == 1 -%}
     @param_name {{"%s%s%s %s"|format("{", e.type, "}", e.param_name)}}  {{d}}
     {% else -%}
     * {{d|indent(l,True)}}
     {% endif -%} {% endfor -%}
     {% endif -%}
     * @return {{"%s%s%s"|format("{", name, "}")}}
     */
    set{{e.method_title}}({{e.param_name}}) {
        {%- if e.external and "Array" not in e.type %}
        this.validateType({{e.external}}, {{e.param_name}});
        {%- endif %}
        this.setParameter({{name}}.{{e.key}}, {{e.param_name}});
        return this;
    }

    /**
     * @return {{"%s%s%s"|format("{", e.type, "}")}}
     */
    get{{e.method_title}}() {
        {%- if e.external %}
        return this.getObject({{e.external}}, {{name}}.{{e.key}});
        {%- else %}
        return this.getParameter({{name}}.{{e.key}});
        {%- endif %}
    }
{% endfor %}
{%- endblock %}
{% block properties %}
{%- for e in params %}
{{name}}.{{e.key}} = {{e.value}};
{%- endfor %}
{%- endblock %}