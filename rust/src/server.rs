use tonic::{transport::Server, Request, Response, Status};
use resilience::unstable_service_server::{UnstableService, UnstableServiceServer};
use resilience::{DataRequest, DataResponse};
use std::env;
use std::time::Duration;
use tokio::time::sleep;
use rand::Rng; 

pub mod resilience {
    tonic::include_proto!("resilience");
}

#[derive(Debug, Default)]
pub struct MyUnstableService;

#[tonic::async_trait]
impl UnstableService for MyUnstableService {
    async fn process_data(
        &self,
        request: Request<DataRequest>,
    ) -> Result<Response<DataResponse>, Status> {
        let chaos_mode = env::var("CHAOS_MODE").unwrap_or_else(|_| "false".to_string()) == "true";
        let payload = request.into_inner().payload;

        if chaos_mode {
            let mut rng = rand::thread_rng();
            let p: f64 = rng.gen(); // Число от 0.0 до 1.0

            // 1. Latency Injection (20%)
            if p < 0.2 {
                println!("[Chaos] Simulating lag (5s) for: {}", payload);
                sleep(Duration::from_secs(5)).await;
            } 
            // 2. Fault Injection (20%)
            else if p < 0.4 {
                println!("[Chaos] Simulating failure for: {}", payload);
                return Err(Status::unavailable("Service temporarily unavailable (Chaos Monkey)"));
            }
        }

        println!("Successfully processed: {}", payload);

        let reply = DataResponse {
            success: true,
            message: format!("Processed: {}", payload),
        };

        Ok(Response::new(reply))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "0.0.0.0:50051".parse()?;
    let service = MyUnstableService::default();

    println!("Rust Server listening on {}", addr);
    println!("Chaos Mode: {}", env::var("CHAOS_MODE").unwrap_or("false".into()));

    Server::builder()
        .add_service(UnstableServiceServer::new(service))
        .serve(addr)
        .await?;

    Ok(())
}
