import sys
import rclpy
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import FollowWaypoints
from nav2_msgs.action._follow_waypoints import FollowWaypoints_GetResult_Response
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from rclpy.node import Node
from rclpy.task import Future


class WaypointsFollower(Node):
    def __init__(self):
        super().__init__("action_client")
        self.action_client: ActionClient = ActionClient(self, FollowWaypoints, "follow_waypoints")
        self.future = Future()
        self.get_result_future = Future()

    def send_goal(self, x: str, y: str):
        goal_msg: FollowWaypoints.Goal = FollowWaypoints.Goal()
        
        # Create PoseStamped object
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.get_clock().now().to_msg()

        # Set position (x, y, z)
        try:
            pose.pose.position.x = float(x)
            pose.pose.position.y = float(y)
            pose.pose.position.z = 0.0  # Ground level
        except ValueError:
            self.get_logger().error(f"Invalid coordinates: {x}, {y}")
            return

        # Set orientation (x, y, z, w) (no rotation)
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = 0.0
        pose.pose.orientation.w = 1.0

        # Append the pose to the goal message
        goal_msg.poses.append(pose)

        # Wait for the action server to be available
        while not self.action_client.wait_for_server(timeout_sec=1):
            self.get_logger().info("FollowWaypoints server is not available!")

        # Send the goal to the action server asynchronously
        self.future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self.future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future: Future):
        goal_handle: ClientGoalHandle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected!")
            return
        self.get_logger().info("Goal Accepted!")

        # Get the result of the goal asynchronously
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)
        self.get_logger().info("Waiting for result...")

    def get_result_callback(self, future: Future):
        result: FollowWaypoints_GetResult_Response = future.result()
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f"Goal succeeded! Missed waypoints: {result.result.missed_waypoints}")
            rclpy.shutdown()  # Shutdown after goal completion
        elif result.status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info("Goal aborted!")

    def feedback_callback(self, msg):
        feedback: FollowWaypoints.Feedback = msg.feedback
        self.get_logger().info(f"Received feedback: {feedback.current_waypoint}")


def main(args=None):
    rclpy.init(args=args)
    node = WaypointsFollower()

    # Ensure correct arguments are passed
    if len(sys.argv) > 2:
        x = sys.argv[1]
        y = sys.argv[2]
        node.send_goal(x, y)
    else:
        node.get_logger().error("Please provide both x and y coordinates as arguments.")
        rclpy.shutdown()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()


if __name__ == "__main__":
    main()
