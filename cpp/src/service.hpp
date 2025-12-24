#pragma once

#include <userver/components/component_list.hpp>
#include <userver/components/loggable_component_base.hpp>
#include <userver/ugrpc/client/client_factory_component.hpp>

// Сгенерированный код gRPC клиента
#include "service_client.usrv.pb.hpp" 

namespace resilience {

class ClientComponent final : public userver::components::LoggableComponentBase {
 public:
  static constexpr std::string_view kName = "resilience-client";

  ClientComponent(const userver::components::ComponentConfig& config,
                  const userver::components::ComponentContext& context);

  // Метод для периодической отправки запросов (для теста)
  void OnAllComponentsLoaded() override;

 private:
  // Клиент, предоставляемый userver
  api::UnstableServiceClient client_;
};

}  // namespace resilience
