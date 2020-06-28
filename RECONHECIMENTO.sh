source /opt/intel/openvino/bin/setupvars.sh
python3 ./face_recognition_demo.py -m_fd models/face-detection-retail-0004/FP32/face-detection-retail-0004.xml -m_lm models/landmarks-regression-retail-0009/FP32/landmarks-regression-retail-0009.xml -m_reid models/face-reidentification-retail-0095/FP32/face-reidentification-retail-0095.xml --verbose -fg data
