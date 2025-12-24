#include <userver/components/minimal_server_component_list.hpp>
#include <userver/clients/dns/component.hpp>
#include <userver/ugrpc/client/client_factory_component.hpp>
#include <userver/utils/daemon_run.hpp>

// Здесь должен быть код вашего компонента Client 
// #include "client_component.hpp"

int main(int argc, char* argv[]) {
  auto component_list = userver::components::MinimalServerComponentList()
                            .Append<userver::clients::dns::Component>()
                            .Append<userver::ugrpc::client::ClientFactoryComponent>();
                            
  // .Append<resilience::ClientComponent>();

  return userver::utils::DaemonMain(argc, argv, component_list);
}
