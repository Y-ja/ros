#ifndef USER_INTERFACE__SRV__ADD_AND_ODD_HPP_
#define USER_INTERFACE__SRV__ADD_AND_ODD_HPP_

#include "builtin_interfaces/msg/time.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"

namespace user_interface
{
namespace srv
{

struct AddAndOdd_Request
{
    using Type = AddAndOdd_Request;

    int32_t inta;  // 첫 번째 정수
    int32_t intb;  // 두 번째 정수

    AddAndOdd_Request()
    : inta(0), intb(0)  // 기본값 설정
    {
    }
};

struct AddAndOdd_Response
{
    using Type = AddAndOdd_Response;

    builtin_interfaces::msg::Time stamp;  // 요청 시각
    int32_t sum;                           // 합계
    std::string odd;                       // 홀짝 여부

    AddAndOdd_Response()
    : sum(0), odd("even")  // 기본값 설정
    {
    }
};

// 요청과 응답을 결합하여 서비스 타입 정의
struct AddAndOdd
{
    using Request = AddAndOdd_Request;
    using Response = AddAndOdd_Response;
};

}  // namespace srv
}  // namespace user_interface

#endif  // USER_INTERFACE__SRV__ADD_AND_ODD_HPP_
