
PROJ = "rpc"

task :test, :python do |t, args|
  p "Running unit tests for #{PROJ}"
  args.with_defaults :python => "python"
  sh "#{args[:python]} -m pytest test"
end
