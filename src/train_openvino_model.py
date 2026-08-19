import os
import numpy as np

def build_and_export_openvino_model():
    """
    Builds a neural network for muscle fatigue classification and exports
    it to Intel OpenVINO Intermediate Representation (IR) format (.xml and .bin).
    """
    print("[INFO] Initializing Intel OpenVINO Model Builder...")
    try:
        import openvino as ov
        import openvino.opset10 as ops
        
        # Input features: [RMS, MAV, VAR, ZCR, MedianFrequency]
        param = ops.parameter([1, 5], dtype=np.float32, name="sEMG_features")

        # Layer 1: Dense Layer (5 -> 16)
        W1 = np.zeros((5, 16), dtype=np.float32)
        W1[0, :] = 0.005   # RMS positive contribution to fatigue
        W1[4, :] = -0.15   # MedianFreq negative contribution (drop in freq = fatigue)
        b1 = np.ones((1, 16), dtype=np.float32) * 0.1

        # Layer 2: Output Layer (16 -> 1)
        W2 = np.ones((16, 1), dtype=np.float32) * 0.15
        b2 = np.zeros((1, 1), dtype=np.float32)

        const_w1 = ops.constant(W1)
        const_b1 = ops.constant(b1)
        fc1 = ops.add(ops.matmul(param, const_w1, False, False), const_b1)
        relu1 = ops.relu(fc1)

        const_w2 = ops.constant(W2)
        const_b2 = ops.constant(b2)
        fc2 = ops.add(ops.matmul(relu1, const_w2, False, False), const_b2)
        sigmoid = ops.sigmoid(fc2)
        res = ops.result(sigmoid, name="fatigue_probability")

        ov_model = ov.Model([res], [param], "RehabArm_Intel_Fatigue_Classifier")
        
        model_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(model_dir, "fatigue_model.xml")
        bin_path = os.path.join(model_dir, "fatigue_model.bin")
        
        ov.save_model(ov_model, xml_path)
        print(f"[SUCCESS] Intel OpenVINO Model IR saved to: {xml_path} and {bin_path}")
        return True
    except Exception as e:
        print(f"[WARNING] OpenVINO export error: {e}")
        return False

class SimpleFatigueClassifier:
    """Fallback classifier or wrapper for OpenVINO inference."""
    def __init__(self):
        self.use_openvino = False
        self.compiled_model = None
        self.device_name = "CPU"
        try:
            import openvino as ov
            model_dir = os.path.dirname(os.path.abspath(__file__))
            xml_path = os.path.join(model_dir, "fatigue_model.xml")
            if not os.path.exists(xml_path):
                build_and_export_openvino_model()
            
            if os.path.exists(xml_path):
                core = ov.Core()
                device = "CPU"
                model = core.read_model(xml_path)
                self.compiled_model = core.compile_model(model, device)
                self.output_layer = self.compiled_model.output(0)
                self.use_openvino = True
                try:
                    self.device_name = core.get_property(device, "FULL_DEVICE_NAME")
                except:
                    self.device_name = device
                print(f"[SUCCESS] Intel OpenVINO Runtime Engine loaded successfully on {device} ({self.device_name})")
        except Exception as e:
            print(f"[INFO] OpenVINO fallback mode: {e}")
            self.use_openvino = False

    def predict_proba(self, X):
        X = np.array(X, dtype=np.float32)
        if len(X.shape) == 1:
            X = np.expand_dims(X, axis=0)
        
        if self.use_openvino and self.compiled_model is not None:
            preds = []
            for sample in X:
                sample_input = np.expand_dims(sample, axis=0)
                prob = float(self.compiled_model([sample_input])[self.output_layer][0][0])
                preds.append([1.0 - prob, prob])
            return np.array(preds)
        else:
            # Rule-based fallback
            preds = []
            for sample in X:
                rms, mav, var, zcr, mf = sample[0], sample[1], sample[2], sample[3], sample[4]
                if mf < 22.0 or rms > 500.0:
                    preds.append([0.1, 0.9])
                else:
                    preds.append([0.9, 0.1])
            return np.array(preds)

    def predict(self, X, threshold=0.75):
        probs = self.predict_proba(X)
        return (probs[:, 1] >= threshold).astype(int)

if __name__ == "__main__":
    build_and_export_openvino_model()
