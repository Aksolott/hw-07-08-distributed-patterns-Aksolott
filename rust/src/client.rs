use std::time::Duration;
use tower::timeout::TimeoutLayer;
use tower::ServiceBuilder;
use resilience::unstable_service_client::UnstableServiceClient;
use resilience::DataRequest;
use tonic::transport::Channel;

pub mod resilience {
    tonic::include_proto!("resilience");
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let server_addr = std::env::var("SERVER_ADDR").unwrap_or("http://localhost:50051".to_string());

    // Создаем канал
    let channel = Channel::from_shared(server_addr)?
        .connect()
        .await?;

    // ЗАДАНИЕ: Добавьте слои (Layers) для Resilience
    let mut client = UnstableServiceClient::new(channel);

    loop {
        let request = tonic::Request::new(DataRequest {
            payload: "ping".into(),
        });

        println!("Sending request...");
        
        // Тут можно реализовать Retry вручную в цикле, если Tower слишком сложен для старта
        match client.process_data(request).await {
            Ok(resp) => println!("Success: {:?}", resp.into_inner().message),
            Err(e) => println!("Error: {:?}", e),
        }

        tokio::time::sleep(Duration::from_secs(1)).await;
    }
}
