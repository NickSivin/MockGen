//
//  ServiceProtocol.swift
//

import Foundation
import CoreBluetooth

protocol ServiceProtocol {
    // Property
    var cacheLifetime: TimeInterval { get set }
    // Read-only property
    var cachedDataSize: Float { get }

    // Simple function
    func refresh()
    // Property between functions
    var cachedDataMaxSize: Double { get set }

    // Function with parameters
    func uploadData(_ data: Data, progressBlock: (Progress) -> Void) async

    // Function with parameters and response
    func requestData(id: String, progressBlock: (Progress) -> Void) async throws -> Data

    // Generic function with parameters and response
    func parseData<Data: Codable, Response>() async throws -> Response where Response : Codable

    // Multiple line function
    func registerDevices<T>(
        deviceA: CBUUID,
        // Internal comment test
        deviceB: CBUUID,
        deviceC: CBUUID
    ) async -> T
}

protocol StorageProtocol {
    // Different property type
    // func_name: setDeviceIDString
    func setDeviceID(_ id: String)
    // func_name: setDeviceIDInt
    func setDeviceID(_ id: Int)
    // func_name: setDeviceIDUUID
    func setDeviceID(_ id: UUID)

    // Different property count
    func saveDeviceInfo(fileName: String)
    // func_name: saveDeviceInfoPath
    func saveDeviceInfo(fileName: String, filePath: String)
    // func_name: saveDeviceInfoPathExtension
    func saveDeviceInfo(fileName: String, filePath: String, fileExtension: String)
}
