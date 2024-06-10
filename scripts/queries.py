GRAPHQL_QUERY = '''
query repository($owner: String!, $name: String!, $per_page: Int!, $afterCursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(
      states: [MERGED, CLOSED]
      orderBy: { field: CREATED_AT, direction: DESC }
      first: $per_page
      after: $afterCursor
    ) {
      edges {
        node {
          title
          number
          state
          createdAt
          closedAt
          mergedAt
          bodyText
          reviewDecision
          reviews {
            totalCount
          }
          files {
            totalCount
          }
          additions
          deletions
          participants {
            totalCount
          }
          comments {
            totalCount
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
'''