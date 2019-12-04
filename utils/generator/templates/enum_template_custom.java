{# not used #}
{% extends "base_template.java" %}
{% block body %}
import java.util.EnumSet;

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
    {{m.method_title}}("{{m.origin}}"),
    {%- endfor %}
    ;

    private final String INTERNAL_NAME;

    private {{name}}(String internalName) {
    	this.INTERNAL_NAME = internalName;
    }

    public String toString() {
        return this.INTERNAL_NAME;
    }

    /**
     * Convert String to {{name}}
     * @param value String
     * @return {{name}}
     */
    public static {{name}} valueForString(String value) {
        if(value == null){
            return null;
        }

    	for ({{name}} anEnum : EnumSet.allOf({{name}}.class)) {
            if (anEnum.toString().equals(value)) {
                return anEnum;
            }
        }
        return null;
    }
}
{% endblock -%}