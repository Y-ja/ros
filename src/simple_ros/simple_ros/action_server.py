import rclpy
import time  # time 모듈 import 추가
from rclpy.node import Node
from rclpy.action import ActionServer
from user_interface.action import Fibonacci


class ActionServerNode(Node):
    def __init__(self):
        super().__init__("action_server_node")
        self.action_server = ActionServer(
            self,
            Fibonacci,
            "fibonacci",
            self.action_callback
        )

    def action_callback(self, goal_handle):
        self.get_logger().info(f"Received goal with step: {goal_handle.request.step}")
        
        # Fibonacci sequence logic
        feedback = Fibonacci.Feedback()
        feedback.temp_seq = [1, 1]  # 피드백 초기화

        for i in range(1, goal_handle.request.step):
            feedback.temp_seq.append(feedback.temp_seq[i-1] + feedback.temp_seq[i])
            self.get_logger().info(f"Publishing feedback: {feedback.temp_seq}")
            goal_handle.publish_feedback(feedback)
            time.sleep(1)  # 피드백 주기 조절

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.seq = feedback.temp_seq  # 결과에 시퀀스 포함
        return result


def main():
    rclpy.init()
    node = ActionServerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down due to keyboard interrupt...")
    except Exception as e:
        node.get_logger().error(f"An error occurred: {e}")
    finally:
        node.destroy_node()
        rclpy.shutdown()
        node.get_logger().info("Node has been shut down.")


if __name__ == "__main__":
    main()
