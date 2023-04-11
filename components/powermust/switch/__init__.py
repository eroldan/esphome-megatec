import esphome.codegen as cg
from esphome.components import switch
import esphome.config_validation as cv
from esphome.const import CONF_BEEPER, ICON_POWER

from .. import CONF_POWERMUST_ID, POWERMUST_COMPONENT_SCHEMA, powermust_ns

DEPENDENCIES = ["uart"]

# CONF_BEEPER = "beeper"
CONF_QUICK_TEST = "quick_test"
CONF_DEEP_TEST = "deep_test"
CONF_TEN_MINUTES_TEST = "ten_minutes_test"

TYPES = {
    CONF_BEEPER: ("Q", "Q"),
    CONF_QUICK_TEST: ("T", "CT"),
    CONF_DEEP_TEST: ("TL", "CT"),
    CONF_TEN_MINUTES_TEST: ("T10", "CT"),
}

PowermustSwitch = powermust_ns.class_("PowermustSwitch", switch.Switch, cg.Component)

PIPSWITCH_SCHEMA = switch.switch_schema(
    PowermustSwitch, icon=ICON_POWER, block_inverted=True
).extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = POWERMUST_COMPONENT_SCHEMA.extend(
    {cv.Optional(type): PIPSWITCH_SCHEMA for type in TYPES}
)


async def to_code(config):
    paren = await cg.get_variable(config[CONF_POWERMUST_ID])

    for type, (on, off) in TYPES.items():
        if type in config:
            conf = config[type]
            var = await switch.new_switch(conf)
            await cg.register_component(var, conf)
            cg.add(getattr(paren, f"set_{type}_switch")(var))
            cg.add(var.set_parent(paren))
            cg.add(var.set_on_command(on))
            if off is not None:
                cg.add(var.set_off_command(off))
