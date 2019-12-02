{% extends "base_template.java" %}
import java.util.EnumSet;

/**
{%- if description %}
 * {{description}}
{%- endif %}
 */
public enum {{enumname}} {
    {%- for p in params %}
    /**{% for d in p.description %}
     * {{d}}{%- endfor %}
     */
    {{p.iname}}("{{p.name}}"),
    {%- endfor %};

    private final String INTERNAL_NAME;

    private {{enumname}}(String internalName) {
    	this.INTERNAL_NAME = internalName;
    }

    public String toString() {
        return this.INTERNAL_NAME;
    }

    /**
     * Convert String to {{enumname}}
     * @param value String
     * @return {{enumname}}
     */
    public static {{enumname}} valueForString(String value) {
        if(value == null){
            return null;
        }

    	for ({{enumname}} anEnum : EnumSet.allOf({{enumname}}.class)) {
            if (anEnum.toString().equals(value)) {
                return anEnum;
            }
        }
        return null;
    }
}