{% extends "base_template.java" %}

{% block body %}
{%- if description %}
/**
 * {{description}}
 */
{%- endif %}
public enum {{name}} {
    {%- for m in methods %}
    {%- if m.description %}
    /**{% for d in m.description %}
     * {{d}}{%- endfor %}
     */
    {%- endif %}
    {{m.method_title}},
    {%- endfor %}
    ;

    /**
     * Convert String to {{name}}
     * @param value String
     * @return {{name}}
     */
    public static {{name}} valueForString(String value) {
        try{
            return valueOf(value);
        }catch(Exception e){
            return null;
        }
    }
}
{% endblock -%}