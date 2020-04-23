// Auto-generated. Do not edit!

// (in-package face_detector.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let people_msgs = _finder('people_msgs');

//-----------------------------------------------------------

class FaceDetectorResult {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.face_positions = null;
    }
    else {
      if (initObj.hasOwnProperty('face_positions')) {
        this.face_positions = initObj.face_positions
      }
      else {
        this.face_positions = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type FaceDetectorResult
    // Serialize message field [face_positions]
    // Serialize the length for message field [face_positions]
    bufferOffset = _serializer.uint32(obj.face_positions.length, buffer, bufferOffset);
    obj.face_positions.forEach((val) => {
      bufferOffset = people_msgs.msg.PositionMeasurement.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type FaceDetectorResult
    let len;
    let data = new FaceDetectorResult(null);
    // Deserialize message field [face_positions]
    // Deserialize array length for message field [face_positions]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.face_positions = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.face_positions[i] = people_msgs.msg.PositionMeasurement.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.face_positions.forEach((val) => {
      length += people_msgs.msg.PositionMeasurement.getMessageSize(val);
    });
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'face_detector/FaceDetectorResult';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'b5dc843df183dbab7f0ab2f5ef5b6f9d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
    #result
    people_msgs/PositionMeasurement[] face_positions
    
    ================================================================================
    MSG: people_msgs/PositionMeasurement
    Header          header
    string          name
    string          object_id
    geometry_msgs/Point pos
    float64         reliability
    float64[9] 	covariance
    byte            initialization
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    # 0: no frame
    # 1: global frame
    string frame_id
    
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new FaceDetectorResult(null);
    if (msg.face_positions !== undefined) {
      resolved.face_positions = new Array(msg.face_positions.length);
      for (let i = 0; i < resolved.face_positions.length; ++i) {
        resolved.face_positions[i] = people_msgs.msg.PositionMeasurement.Resolve(msg.face_positions[i]);
      }
    }
    else {
      resolved.face_positions = []
    }

    return resolved;
    }
};

module.exports = FaceDetectorResult;
