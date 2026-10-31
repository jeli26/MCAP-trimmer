import argparse
from pathlib import Path
from mcap.reader import make_reader
from mcap.writer import Writer

parser = argparse.ArgumentParser(description="Trim an MCAP file based on start and end times")

parser.add_argument('-p', '--path', type=Path, required=True, help="the path to the MCAP file")
parser.add_argument('-s', '--start', type=float, default=0.0, help="starting elapsed time in seconds, inclusive bound")
parser.add_argument('-e', '--end', type=float, default=None, help="ending elapsed time in seconds, inclusive bound")
parser.add_argument('-ia', '--include-all', action="store_true", help="enable including all attatchments and metadata")

args = parser.parse_args()

args.path = args.path.resolve()
if not args.path.is_file():
    parser.error("Path to MCAP file does not exist")

with open(args.path, "rb") as input_file:
    reader = make_reader(input_file)
    with open(args.path.with_stem(args.path.stem + "_trimmed"), "wb") as output_file:
        writer = Writer(output_file)
        writer.start(reader.get_header().profile, reader.get_header().library)
        if (args.include_all):
            for attatchment in reader.iter_attachments():
                writer.add_attachment(attatchment.create_time, attatchment.log_time, attatchment.name, attatchment.media_type, attatchment.data)
            for metadata in reader.iter_metadata():
                writer.add_metadata(metadata.name, metadata.metadata)

        _, _, first_message = next(reader.iter_messages(log_time_order=True), None)
        start_timestamp = None
        end_timestamp = None
        if (first_message is not None):
            start_timestamp = first_message.log_time + int(args.start * 1000000000)
            end_timestamp = first_message.log_time + int(args.end * 1000000000) if args.end is not None else None 

        schema_map = {}
        channel_map = {}

        for schema, channel, message in reader.iter_messages(starting_at=start_timestamp, ending_at=end_timestamp):
            if schema.id not in schema_map:
                schema_map[schema.id] = writer.register_schema(schema.name, schema.encoding, schema.data)

            if channel.id not in channel_map:
                channel_map[channel.id] = writer.register_channel(topic=channel.topic, message_encoding=channel.message_encoding, schema_id=schema_map[channel.schema_id], metadata=channel.metadata)

            writer.add_message(channel_id=channel_map[message.channel_id], log_time=message.log_time, data=message.data, publish_time=message.publish_time, sequence=message.sequence)

        writer.finish()