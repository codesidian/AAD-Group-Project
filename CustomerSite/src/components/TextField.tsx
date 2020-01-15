import * as React from "react";

type TextFieldProps = {
    label: string;
    onTextChange: (text: string) => void;
    text: string;
};

export default class TextField extends React.Component<TextFieldProps> {
    handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.props.onTextChange(e.target.value);
    }

    render() {
        const text = this.props.text;
        const label = this.props.label;
        return <div className="form-group">
            <label>{label}</label>
            <input value={text}
                onChange={this.handleChange}
                type="text"
                className="form-control" />
        </div>
    }
}
