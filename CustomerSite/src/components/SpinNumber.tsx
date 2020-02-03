/*
<div class="input-group">
  <div class="input-group-prepend">
    <button class="btn btn-outline-secondary" type="button">Button</button>
  </div>
  <input type="text" class="form-control" placeholder="Recipient's username" aria-label="Recipient's username" aria-describedby="basic-addon2">
  <div class="input-group-append">
    <button class="btn btn-outline-secondary" type="button">Button</button>
  </div>
</div>
*/

import * as React from "react";
import Cart from "../data/Cart";
import { SaleItem } from "../data/Types";

type SpinNumberProps = {
    value: number;
    onValueChange: (value: number) => void;
};

type SpinNumberState = {
    inputValue: number;
    editing: boolean;
}

export default class SpinNumber extends React.Component<SpinNumberProps, SpinNumberState> {
    constructor(props: Readonly<SpinNumberProps>) {
        super(props);
        this.state = { inputValue: props.value, editing: false };
    }

    onValueBlur = (e: React.FocusEvent<HTMLInputElement>) => {
        this.setState({ editing: false });
        this.props.onValueChange(this.state.inputValue);
    }

    onValueFocus =(e: React.FocusEvent<HTMLInputElement>) => {
        this.setState({ editing: true });
    } 

    onValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({ inputValue: e.target.valueAsNumber });
    }

    onIncrement = () => {
        this.props.onValueChange(this.props.value + 1);
    }

    onDecrement = () => {
        this.props.onValueChange(this.props.value - 1);
    }

    static getDerivedStateFromProps(props: SpinNumberProps, state: SpinNumberState): Partial<SpinNumberState> | null {
        // props hold true value of field, however we use a temporary value to make editing easier
        // if not editing use the true value
        if (!state.editing) {
            return { inputValue: props.value };
        } else {
            return null;
        }
    }

    render() {
        return <div className="input-group">
        <div className="input-group-prepend">
          <button className="btn btn-outline-secondary" type="button" onClick={this.onDecrement}>-</button>
        </div>
        <input type="number" className="form-control" value={this.state.inputValue} onChange={this.onValueChange} onBlur={this.onValueBlur} onFocus={this.onValueFocus}/>
        <div className="input-group-append">
          <button className="btn btn-outline-secondary" type="button" onClick={this.onIncrement}>+</button>
        </div>
      </div>;
    }
}
