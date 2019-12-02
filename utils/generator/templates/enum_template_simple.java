{% extends "base_template.java" %}

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
    {{p.name}},
    {%- endfor %};

    /**
     * Convert String to {{enumname}}
     * @param value String
     * @return {{enumname}}
     */
    public static {{enumname}} valueForString(String value) {
        try{
            return valueOf(value);
        }catch(Exception e){
            return null;
        }
    }
}