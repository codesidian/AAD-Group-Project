import * as React from "react";
import jsQR from "jsqr";

type QRScannerProps = {
    qrScanned: (qrcode: string) => void;
}

type QRScannerState = {
    scanningCanvas: HTMLCanvasElement;
    running: boolean;
    stream?: MediaStream;
}

export default class QRScanner extends React.Component<QRScannerProps, QRScannerState> {
    state: QRScannerState = {
        scanningCanvas: document.createElement("canvas"),
        running: true,
    }

    render() {
        return <video id="qrscan" style={{width: "100%", maxWidth: "360px"}} autoPlay></video>;
    }

    onRequestAnimationFrame = (timestep : DOMHighResTimeStamp) => {
        const canvas = this.state.scanningCanvas;
        const stream = this.state.stream;
        
        if (!this.state.running) {
            return;
        }

        // HACK
        const video = document.getElementById("qrscan") as HTMLVideoElement | null;

        if (video === null) {
            requestAnimationFrame(this.onRequestAnimationFrame);
            return;
        }

        if (video.srcObject === null) {
            video.srcObject = stream as MediaStream;
        }

        if (stream !== undefined) {
            const settings = stream.getVideoTracks()[0].getSettings();
            canvas.width = settings.width as number;
            canvas.height = settings.height as number;

            const context = canvas.getContext("2d");
            context?.drawImage(video, 0, 0, canvas.width, canvas.height);

            const code = jsQR(context?.getImageData(0, 0, canvas.width, canvas.height).data as Uint8ClampedArray, canvas.width, canvas.height);

            if (code) {
                this.props.qrScanned(code.data);
            }
        }
        
        requestAnimationFrame(this.onRequestAnimationFrame);
    }

    async componentDidMount() {
        this.setState({
            stream: await navigator.mediaDevices.getUserMedia({video: {width: 360, aspectRatio: 0.5625, facingMode: 'environment'}})
        });
        requestAnimationFrame(this.onRequestAnimationFrame);
    }

    componentWillUnmount() {
        this.setState({running: false});
    }
}
