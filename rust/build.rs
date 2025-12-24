fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Компиляция proto файла при сборке
    // Путь ../proto должен быть доступен
    tonic_build::compile_protos("../proto/service.proto")?;
    Ok(())
}
