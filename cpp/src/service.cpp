#include "service.hpp"
#include <userver/yaml_config/merge_schemas.hpp>
#include <userver/engine/sleep.hpp>

namespace resilience {

ClientComponent::ClientComponent(const userver::components::ComponentConfig& config,
                                 const userver::components::ComponentContext& context)
    : userver::components::LoggableComponentBase(config, context),
      client_(context.FindComponent<userver::ugrpc::client::ClientFactoryComponent>()
                  .GetClientFactory()
                  .MakeClient<api::UnstableServiceClient>("unstable-service-client")) {}

void ClientComponent::OnAllComponentsLoaded() {
    // Бесконечный цикл запросов
    while (true) {
        api::DataRequest request;
        request.set_payload("ping");

        // Контекст запроса. Timeout и Retry будут применены автоматически из config.yaml!
        auto context = std::make_unique<grpc::ClientContext>();

        try {
            auto call = client_.ProcessData(request, std::move(context));
            api::DataResponse response = call.Finish();
            LOG_INFO() << "Success: " << response.message();
        } catch (const std::exception& ex) {
            LOG_ERROR() << "Error: " << ex.what();
        }
        
        userver::engine::SleepFor(std::chrono::seconds(1));
    }
}

}  // namespace resilience
