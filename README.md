# Carrier - A Messaging Service
Carrier is a personal project that I worked on throughout the second half of my last semester at UVM, and presented at the winter 2024 UVM CS fair. The project provides a lightweight messaging service.

## Structure
To facilitate the connections between users, Carrier requires both a server, and clients. Using TCP sockets generated with asyncio, the clients are able to send messages to the server, which stores those messages in a SQLite database, and then passes the message along to its intended recipient. To ensure that messages end up with the right individuals, Carrier employs a simple account system. When a client first connects to the server, it will send a username and password, which is then checked (on the server side) against the SQLite database.

## Area's for further improvement
* Encryption: due to the limits of my own manpower, and the swiftly approaching CS fair deadline, I opted not to add encryption to the communications from server and client. However, were I to return to this project in the future, that would be number 1 on the agenda.
* Inconsistency introduced by the TCP sockets: when testing the program I ran into several issues pertaining to the nature of TCP sockets. Specifically, since TCP sockets cannot gurantee that the whole message has been received, messages that were large could be clipped, and messages that were received back to back could be merged. I believe this issue could be resolved by either implementing a smarter set of flags on the messages, or changing to UDP sockets
* Aesthetics: One of my first ideas while working on this project was to add user-specific colors, so that a user could choose what color their name would appear as in their own and other's chat windows. While a less important issue, I would still love to be able to implement that functionality
