import pandas as pd
import numpy as np
import pyomo.environ as py
import os
import NoCopHH_mod_plot_IAMC as plot_IAMC


def write_IAMC(output_df, model, scenario, region, variable, unit, time, values):

    if isinstance(values, list):
        _df = pd.DataFrame(
            {
                "model": model,
                "scenario": scenario,
                "region": region,
                "variable": variable,
                "unit": unit,
                "year": time,
                "value": values,
            }
        )
    else:
        _df = pd.DataFrame(
            {
                "model": model,
                "scenario": scenario,
                "region": region,
                "variable": variable,
                "unit": unit,
                "year": time,
                "value": values,
            },
            index=[0],
        )

    output_df = output_df.append(_df)
    return output_df


def write_results_to_ext_iamc_format(m, res_dir):
    output_iamc = pd.DataFrame()
    _scenario = "Baseline"
    _model = "NoCopHH-modv1.0"
    _region = "Norway"
    _unit = "EUR"
    _time = "2021"
    output_iamc = pd.DataFrame()

    # Spot markt revenues
    _value = np.around(py.value(m.revenues_spot), 0)
    output_iamc = write_IAMC(
        output_iamc, _model, _scenario, _region, "Day-Ahead", _unit, _time, _value
    )
    # Base future revenues
    _value = np.around(py.value(m.revenues_future), 0)
    output_iamc = write_IAMC(
        output_iamc, _model, _scenario, _region, "Future contract", _unit, _time, _value
    )
    # Hydrogen revenues
    _value = np.around(py.value(m.revenues_H2), 0)
    output_iamc = write_IAMC(
        output_iamc, _model, _scenario, _region, "Hydrogen", _unit, _time, _value
    )

    output_iamc.to_excel(os.path.join(res_dir, "IAMC_annual.xlsx"), index=False)

    _unit = "MWh"
    _time = [_t for _t in m.set_time]
    output_iamc = pd.DataFrame()

    # Quantity future
    _value = []
    for _t in m.set_time:
        _value.append(np.around(py.value(m.v_q_future[_t]), 0))
    output_iamc = write_IAMC(
        output_iamc, _model, _scenario, _region, "Future contract", _unit, _time, _value
    )
    # Quantity day-ahead
    _value = []
    for _t in m.set_time:
        _value.append(np.around(py.value(m.v_q_spot[_t]), 0))
    output_iamc = write_IAMC(
        output_iamc, _model, _scenario, _region, "Day-Ahead", _unit, _time, _value
    )
    # Quantity hydrogen
    _value = []
    for _t in m.set_time:
        _value.append(np.around(py.value(m.v_q_H2[_t]), 0))
    output_iamc = write_IAMC(
        output_iamc, _model, _scenario, _region, "Hydrogen", _unit, _time, _value
    )

    output_iamc.to_excel(os.path.join(res_dir, "IAMC_hourly.xlsx"), index=False)

    _value = []
    for _t in m.set_time:
        _value.append(np.around(py.value(m.v_q_fossil[_t]), 0))
    output_iamc = write_IAMC(
        output_iamc, _model, _scenario, _region, "Conventional", _unit, _time, _value
    )

    output_iamc.to_excel(os.path.join(res_dir, "IAMC_supply.xlsx"), index=False)

    plot_IAMC.plot_results(res_dir)

    # Write shadow price and projecte shadow price to result file
    output_iamc = pd.DataFrame()
    _value = []
    for _t in m.set_time:
        _value.append(np.around(-py.value(m.dual_lambda_load[_t]), 2))
    output_iamc = write_IAMC(
        output_iamc, _model, _scenario, _region, "Shadow price", _unit, _time, _value
    )

    output_iamc.to_excel(
        os.path.join(res_dir, "IAMC_Profitability_Gap.xlsx"), index=False
    )
