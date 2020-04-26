#include "spdlog/spdlog.h"
#include "spdlog/sinks/basic_file_sink.h"

#include <iostream>

int main()
{

  std::cout << "spdlog test" << std::endl;

  spdlog::info("Sample Info output.");
  spdlog::warn("Sample Warn output.");
  spdlog::error("Sample Error output.");

  auto filelog = spdlog::basic_logger_mt("sample-logger", "sample-log.txt");

  filelog.get()->info("Sample Info output.");
  filelog.get()->warn("Sample Warn output.");
  filelog.get()->error("Sample Error output.");

  return 0;
}