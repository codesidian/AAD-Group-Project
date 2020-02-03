import * as React from "react";

type PressToScanProps = {
    pressed: () => void;
}

export default class PressToScan extends React.Component<PressToScanProps> {
    onClick = () => {
        this.props.pressed();
    }

    render() {
        return <div className="text-center text-light bg-dark p-4" onClick={this.onClick}>Press here to scan</div>
    }
}
