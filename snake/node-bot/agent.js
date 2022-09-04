process.stdin.on("data", raw_data => {
  raw_data = raw_data.toString()
  data = JSON.parse(raw_data)
  process.stdout.write(JSON.stringify(data))
})
