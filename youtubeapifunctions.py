from googleapiclient.errors import HttpError


def get_all_playlists(service):
    request = service.playlists().list(
        part='snippet',
        mine=True
    )
    response = request.execute()
    playlists = []
    for item in response['items']:
        playlists.append({
            'id': item['id'],
            'name': item['snippet']['title']
        })
    return playlists


def remove_video_from_playlist(service, playlist_item_id):
    service.playlistItems().delete(id=playlist_item_id).execute()


def get_video_views_playlist(service, playlist):
    videos = []
    playlist_item_ids = []
    nextPageToken = None
    while True:
        pl_request = service.playlistItems().list(
            part='contentDetails',
            playlistId=playlist,
            maxResults=50,
            pageToken=nextPageToken
        )
        pl_response = pl_request.execute()

        vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

        playlist_item_ids += [item['id'] for item in pl_response['items']]

        vid_request = service.videos().list(
            part="statistics",
            id=','.join(vid_ids)
        )
        vid_response = vid_request.execute()

        for item in vid_response['items']:
            videos.append({
                'playlist_item_id': None,
                'views': int(item['statistics']['viewCount']),
                'id': item['id']
            })

        nextPageToken = pl_response.get('nextPageToken')
        if not nextPageToken:
            break
    for index in range(len(videos)):
        videos[index]['playlist_item_id'] = playlist_item_ids[index]

    return videos


def get_video_name_playlist(service, playlist):
    videos = []
    nextPageToken = None
    while True:
        pl_request = service.playlistItems().list(
            part='snippet',
            playlistId=playlist,
            maxResults=50,
            pageToken=nextPageToken
        )
        pl_response = pl_request.execute()

        for item in pl_response['items']:
            videos.append({
                'id': item['snippet']['resourceId']['videoId'],
                'name': item['snippet']['title'],
                'playlist_item_id': item['id']
            })

        nextPageToken = pl_response.get('nextPageToken')
        if not nextPageToken:
            break

    return videos


def get_video_duration_playlist(service, playlist):
    videos = []
    playlist_item_ids = []
    nextPageToken = None
    while True:
        pl_request = service.playlistItems().list(
            part='contentDetails',
            playlistId=playlist,
            maxResults=50,
            pageToken=nextPageToken
        )
        pl_response = pl_request.execute()

        vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

        playlist_item_ids += [item['id'] for item in pl_response['items']]

        vid_request = service.videos().list(
            part='contentDetails',
            id=','.join(vid_ids)
        )
        vid_response = vid_request.execute()

        for item in vid_response['items']:
            duration = str(item['contentDetails']['duration'][2:])
            days = int(duration[:duration.index('D')]) if duration.__contains__('D') else 0
            hours = int(duration[duration.index('D') + 1 if duration.__contains__('D') else 0: duration.index('H')]) + days * 24 if duration.__contains__('H') else 0
            minutes = int(duration[duration.index('H') + 1 if duration.__contains__('H') else 0: duration.index('M')]) + hours * 60 if duration.__contains__('M') else 0
            seconds = int(duration[duration.index('M') + 1 if duration.__contains__('M') else 0: duration.index('S')]) + minutes * 60
            videos.append({
                'playlist_item_id': None,
                'duration': seconds,
                'id': item['id']
            })

        nextPageToken = pl_response.get('nextPageToken')
        if not nextPageToken:
            break
    for index in range(len(videos)):
        videos[index]['playlist_item_id'] = playlist_item_ids[index]

    return videos


def get_video_upload_time_playlist(service, playlist):
    videos = []
    playlist_item_ids = []
    nextPageToken = None
    while True:
        pl_request = service.playlistItems().list(
            part='contentDetails',
            playlistId=playlist,
            maxResults=50,
            pageToken=nextPageToken
        )
        pl_response = pl_request.execute()

        vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

        playlist_item_ids += [item['id'] for item in pl_response['items']]

        vid_request = service.videos().list(
            part="snippet",
            id=','.join(vid_ids)
        )
        vid_response = vid_request.execute()

        for item in vid_response['items']:
            upload_time = item['snippet']['publishedAt'].replace('Z', '').replace('T', '-').replace(':', '-').split('-')
            years = int(upload_time[0]) - 2000
            months = int(upload_time[1]) + years * 12
            days = int(upload_time[2]) + months * 31
            hours = int(upload_time[3]) + days * 24
            minutes = int(upload_time[4]) + hours * 60
            seconds = int(upload_time[5]) + minutes * 60
            videos.append({
                'playlist_item_id': None,
                'upload_time': int(seconds),
                'id': item['id']
            })

        nextPageToken = pl_response.get('nextPageToken')
        if not nextPageToken:
            break
    for index in range(len(videos)):
        videos[index]['playlist_item_id'] = playlist_item_ids[index]

    return videos


def get_video_add_time_playlist(service, playlist):
    videos = []
    nextPageToken = None
    while True:
        pl_request = service.playlistItems().list(
            part='snippet',
            playlistId=playlist,
            maxResults=50,
            pageToken=nextPageToken
        )
        pl_response = pl_request.execute()

        for item in pl_response['items']:
            add_time = item['snippet']['publishedAt'].replace('Z', '').replace('T', '-').replace(':', '-').split('-')
            years = int(add_time[0]) - 2000
            months = int(add_time[1]) + years * 12
            days = int(add_time[2]) + months * 31
            hours = int(add_time[3]) + days * 24
            minutes = int(add_time[4]) + hours * 60
            seconds = int(add_time[5]) + minutes * 60
            videos.append({
                'playlist_item_id': item['id'],
                'add_time': int(seconds),
                'id': item['snippet']['resourceId']['videoId']
            })

        nextPageToken = pl_response.get('nextPageToken')
        if not nextPageToken:
            break

    return videos


def sort_playlist(service, videos, playlist_id):
    try:
        for index in range(len(videos)):
            update_request = service.playlistItems().update(
                part='snippet',
                body={
                    "id": videos[index]['playlist_item_id'],
                    "snippet": {
                        "playlistId": playlist_id,
                        "position": index,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": videos[index]['id']
                        }
                    }
                }
            )
            update_request.execute()
        return 'Playlist Sorted!'
    except HttpError:
        return 'There are no Quotas left, try again tomorrow!'


def sort_playlist_by_views(service, playlist, order):
    videos = get_video_views_playlist(service, playlist['id'])
    videos.sort(key=lambda vid: vid['views'], reverse=order)
    sort_playlist(service, videos, playlist['id'])


def sort_playlist_by_upload_time(service, playlist, order):
    videos = get_video_upload_time_playlist(service, playlist['id'])
    videos.sort(key=lambda vid: vid['upload_time'], reverse=order)
    sort_playlist(service, videos, playlist['id'])


def sort_playlist_by_add_time(service, playlist, order):
    videos = get_video_add_time_playlist(service, playlist['id'])
    videos.sort(key=lambda vid: vid['add_time'], reverse=order)
    sort_playlist(service, videos, playlist['id'])


def sort_playlist_by_video_duration(service, playlist, order):
    videos = get_video_duration_playlist(service, playlist['id'])
    videos.sort(key=lambda vid: vid['duration'], reverse=order)
    sort_playlist(service, videos, playlist['id'])


def sort_playlist_by_alphabet(service, playlist, order):
    videos = get_video_name_playlist(service, playlist['id'])
    videos.sort(key=lambda vid: vid['name'], reverse=order)
    sort_playlist(service, videos, playlist['id'])


def clean_playlist(service, playlist):
    video_ids = []
    token = None
    count = 0
    try:
        while True:
            id_request = service.playlistItems().list(
                part='contentDetails',
                playlistId=playlist['id'],
                maxResults=50,
                pageToken=token
            )
            id_response = id_request.execute()
            video_ids += [video['contentDetails']['videoId'] for video in id_response['items']]
            request = service.videos().list(
                part='snippet',
                id=','.join([video['contentDetails']['videoId'] for video in id_response['items']])
            )
            response = request.execute()
            diff = len(id_response['items']) - len(response['items'])
            if diff > 0:
                count += diff
                for index in range(len(id_response['items'])):
                    if not str(response['items']).__contains__(id_response['items'][index]['contentDetails']['videoId']):
                        print(f"Deleting https://youtu.be/{id_response['items'][index]['contentDetails']['videoId']}.....")
                        remove_video_from_playlist(service, id_response['items'][index]['id'])
            if str(id_response).__contains__('nextPageToken'):
                token = id_response['nextPageToken']
            else:
                return 'Playlist Cleaned!'
    except HttpError:
        return 'There are no Quotas left, try again tomorrow!'
